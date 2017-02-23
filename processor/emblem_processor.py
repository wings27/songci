import logging
import multiprocessing
import operator
from itertools import repeat

import pymongo

from mapreduce.driver import MapReduceDriver
from mapreduce.emblem_finals import EmblemFinals
from mapreduce.emblem_freq import EmblemFreq
from nlp.emblem import Emblem
from processor.data_source import MongoDataSource


class EmblemProcessor:
    """
    Processor that deals with emblems.

    It is normally used to extract emblems from a list of songci contents,
    and then save them to the data source,
    along with some other fields such as the term-frequency of emblems.

    The data source is supposed be schema-free (e.g. MongoDB),
    so the schema of emblem is defined, or rather described, within this class
    in order to provide flexibility.

    The schema of emblem:
        - name
        - freq_rate
        - finals
            - pinyin
            - rhyme
            - tones
    """
    COLLECTION_EMBLEM = 'emblem'
    COLLECTION_SONGCI_CONTENT = 'songci_content'

    data_source = MongoDataSource()

    logger = logging.getLogger('emblem_stat')
    logging.basicConfig(level=logging.INFO)

    def gen_freq_rate(self):
        """
        This function does two things:
        1. Extract emblems from a list of songci contents.
        2. Generate field of freq_rate for those emblems.
        The field of freq_rate is the term-frequency rate of an emblem,
        whose value defines whether a word is an emblem.

        :return: list of tuples(emblem_name, freq_rate)
        """
        map_reduce_driver = MapReduceDriver(EmblemFreq.map_fn, EmblemFreq.reduce_fn)
        songci_list = self.data_source.find(self.COLLECTION_SONGCI_CONTENT)

        emblem_stat_list = map_reduce_driver(Emblem(songci_list).emblem_list())
        emblem_stat_list.sort(key=operator.itemgetter(1), reverse=True)

        def map_to_freq_rate(freq_stat_list):
            min_freq_allowed = 2
            total_len = len(freq_stat_list)

            ret = []
            prev_freq = prev_freq_rate = 0  # cache previous quotient (a.k.a. freq) to improve performance
            for freq_stat in freq_stat_list:
                name, freq = freq_stat
                if freq < min_freq_allowed:
                    break
                freq_rate = prev_freq_rate if freq == prev_freq else freq / total_len
                ret.append((name, freq_rate))

                prev_freq = freq
                prev_freq_rate = freq_rate
            return ret

        result_to_be_saved = map_to_freq_rate(emblem_stat_list)

        return result_to_be_saved

    def gen_finals(self):
        """
        Generate field of finals for emblems from self.data_source,
        where finals is a dict whose keys are pinyin, rhyme, tones, etc.

        :return: list of tuples(emblem_name, finals)
        """
        map_reduce_driver = MapReduceDriver(EmblemFinals.map_fn, EmblemFinals.reduce_fn, workers=4)
        emblem_list = self.data_source.find(
            self.COLLECTION_EMBLEM,
            projection=['name'],
            sort=[('freq_rate', pymongo.DESCENDING)])
        emblem_finals_stat = map_reduce_driver((emblem['name'] for emblem in emblem_list))

        result_to_be_saved = [(name, {
            'pinyin': finals.pinyin,
            'rhyme': finals.rhyme,
            'tones': finals.tones,
        }) for (name, finals) in emblem_finals_stat]

        return result_to_be_saved

    def save_emblems_field(self, emblem_with_field_list, field_name, index=True):
        """
        Save emblems along with provided field,
        where field can be any of the types that self.data_source supports.

        :param emblem_with_field_list: tuple of (emblem_name, field)
        :param field_name: the name of that field

        :return: None
        """
        total_len = len(emblem_with_field_list)
        self.logger.info('Saving field [%s], total=%d', field_name, total_len)

        workers = (multiprocessing.cpu_count() or 1) * 4
        emblem_freq_chunks = MapReduceDriver.chunks(emblem_with_field_list, int(total_len / workers))

        with multiprocessing.Pool(processes=workers) as pool:
            pool.starmap(self._save_emblems_field, zip(emblem_freq_chunks, repeat(field_name)))

        if index:
            self.data_source.create_index(self.COLLECTION_EMBLEM, 'name', unique=True)
            self.data_source.create_index(self.COLLECTION_EMBLEM, field_name)
            field = emblem_with_field_list[0][1]
            if isinstance(field, dict):
                for key in field.keys():
                    self.data_source.create_index(self.COLLECTION_EMBLEM, field_name + '.' + key)

    def _save_emblems_field(self, emblem_with_field_list, field_name):
        for (emblem_name, field) in emblem_with_field_list:
            self.data_source.save(self.COLLECTION_EMBLEM, {'name': emblem_name}, {field_name: field})


if __name__ == '__main__':
    processor = EmblemProcessor()
    processor.save_emblems_field(processor.gen_freq_rate(), 'freq_rate')
    processor.save_emblems_field(processor.gen_finals(), 'finals')
