import logging
import operator
import os

from mapreduce.driver import MapReduceDriver
from mapreduce.emblem_finals import EmblemFinals
from mapreduce.emblem_freq import EmblemFreq
from nlp.emblem import Emblem


class EmblemProcessor:
    """
    Processor that deals with emblems.

    It is normally used to extract emblems from a list of songci contents,
    and then save them back to the data accessing object,
    along with some other fields such as the term-frequency of emblems.

    The schema of an emblem:
        - name
        - freq_rate
        - finals
            - pinyin
            - rhyme
            - tones
    """

    logger = logging.getLogger('processor.EmblemProcessor')
    logging.basicConfig(level=logging.INFO)

    def __init__(self, emblem_dao):
        self.emblem_dao = emblem_dao
        self.songci_list = emblem_dao.load_songci_list()

        if 'load_emblem_list' in dir(emblem_dao):
            self._emblem_list = emblem_dao.load_emblem_list()

    @property
    def emblem_list(self):
        if not self._emblem_list:
            self.gen_freq_rate()
        return self._emblem_list

    def gen_freq_rate(self):
        """
        Generate frequency rates for all the emblems from songci_list.
        The field freq_rate is the term-frequency rate of a word (raw_emblem),
        and this field determines whether a word is recognized as an emblem.

        :return: list of tuples(emblem_name, freq_rate)
        """
        raw_emblem_list = Emblem(self.songci_list).raw_emblem_list()
        self.logger.info(
            'Generating frequency rates, total=%d', len(raw_emblem_list))
        map_reduce_driver = MapReduceDriver(
            EmblemFreq.map_fn, EmblemFreq.reduce_fn)
        emblem_stat_list = map_reduce_driver(raw_emblem_list)
        emblem_stat_list.sort(key=operator.itemgetter(1), reverse=True)

        def map_to_freq_rate(freq_stat_list):
            min_freq_allowed = 2
            total_len = len(freq_stat_list)

            ret = []
            # cache previous quotient (a.k.a. freq) to improve performance
            prev_freq_rate = prev_freq = 0
            for freq_stat in freq_stat_list:
                name, freq = freq_stat
                if freq < min_freq_allowed:
                    break
                freq_rate = prev_freq_rate if freq == prev_freq \
                    else freq / total_len
                ret.append((name, freq_rate))

                prev_freq = freq
                prev_freq_rate = freq_rate
            return ret

        result_to_be_saved = map_to_freq_rate(emblem_stat_list)
        self._emblem_list = [name for (name, freq_rate) in result_to_be_saved]

        return result_to_be_saved

    def gen_finals(self):
        """
        Generate finals for emblems.
        Finals are dictionaries whose keys are pinyin, rhyme, tones, etc.

        :return: list of tuples(emblem_name, finals)
        """
        emblem_list = self.emblem_list
        self.logger.info(
            'Generating finals, total=%d', len(emblem_list))
        workers = (os.cpu_count() or 1) << 3
        map_reduce_driver = MapReduceDriver(
            EmblemFinals.map_fn, EmblemFinals.reduce_fn, workers=workers)
        emblem_finals_stat = map_reduce_driver(emblem_list)

        result_to_be_saved = [(name, {
            'pinyin': finals.pinyin,
            'rhyme': finals.rhyme,
            'tones': finals.tones,
        }) for (name, finals) in emblem_finals_stat]

        return result_to_be_saved
