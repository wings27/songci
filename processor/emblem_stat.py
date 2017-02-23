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
    COLLECTION_EMBLEM = 'emblem'
    COLLECTION_SONGCI_CONTENT = 'songci_content'

    data_source = MongoDataSource()

    logger = logging.getLogger('emblem_stat')
    logging.basicConfig(level=logging.INFO)

    def stat_freq_rate(self):
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

        emblem_stat_list = map_to_freq_rate(emblem_stat_list)
        self._save_emblems(emblem_stat_list, 'freq_rate')

    def stat_finals(self):
        map_reduce_driver = MapReduceDriver(EmblemFinals.map_fn, EmblemFinals.reduce_fn, workers=4)
        emblem_list = self.data_source.find(
            self.COLLECTION_EMBLEM,
            projection=['name'],
            sort=[('freq_rate', pymongo.DESCENDING)])
        emblem_finals_stat = map_reduce_driver((emblem['name'] for emblem in emblem_list))

        self._save_emblems([(name, {
            'pinyin': finals.pinyin,
            'rhyme': finals.rhyme,
            'tones': finals.tones,
        }) for (name, finals) in emblem_finals_stat], 'finals')

    def _save_emblems(self, emblem_stat_list, stat_field_name):
        self.logger.info('Saving field [%s], total=%d', stat_field_name, len(emblem_stat_list))
        total_len = len(emblem_stat_list)
        workers = (multiprocessing.cpu_count() or 1) * 4
        emblem_freq_chunks = MapReduceDriver.chunks(emblem_stat_list, int(total_len / workers))

        with multiprocessing.Pool(processes=workers) as pool:
            pool.starmap(self._save_emblem_stat, zip(emblem_freq_chunks, repeat(stat_field_name)))

        self.data_source.create_index(self.COLLECTION_EMBLEM, 'name', unique=True)
        self.data_source.create_index(self.COLLECTION_EMBLEM, stat_field_name)

    def _save_emblem_stat(self, emblem_stat, stat_field_name):
        for (emblem_name, stat) in emblem_stat:
            self.data_source.save(self.COLLECTION_EMBLEM, {'name': emblem_name}, {stat_field_name: stat})


if __name__ == '__main__':
    processor = EmblemProcessor()
    processor.stat_freq_rate()
    processor.stat_finals()
