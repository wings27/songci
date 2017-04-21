import logging
import re
from collections import deque
from io import StringIO

from mapreduce.driver import MapReduceDriver
from nlp import pingze
from nlp.pingze import is_yun, to_tones_regex
from nlp.verse import sub_verses
from tune_data import load_tune


class WordPattern:
    def __init__(self, length, tones_regex, rhyme=None) -> None:
        self.length = length
        self.tones_regex = tones_regex
        self.rhyme = rhyme

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def fetch_word(self, data_source_dao) -> (str, int):
        where = {}
        if self.tones_regex:
            where["finals.tones"] = re.compile('^%s$' % self.tones_regex)
        if self.rhyme:
            where["finals.rhyme"] = self.rhyme

        word = data_source_dao.random_emblem_name(where).next()['name']
        self.logger.debug('fetch_word: (%s,%s) -> %s',
                          self.tones_regex, self.rhyme, word)
        return word, self.length


class SongciWriter:
    def __init__(self, tune_name, rhyme, data_source_dao) -> None:
        self.tune_name = tune_name
        self.rhyme = rhyme
        self.data_source_dao = data_source_dao

        self._tune = load_tune(self.tune_name)
        self._word_patterns = None

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def write_new(self) -> (str, str):
        if not self._tune.pattern:
            raise ValueError(
                'pattern for tune [%s] is empty.' % self.tune_name)
        self._analyze()

        with StringIO() as songci_io:
            pointer = 0
            while pointer < len(self._tune.pattern):
                char = self._tune.pattern[pointer]
                if char in pingze.ping_ze_def.values():
                    word, pointer_step = self._next_word_pattern().fetch_word(
                        self.data_source_dao)
                else:
                    word, pointer_step = char, len(char)
                pointer += pointer_step
                songci_io.write(word)

            return self._tune.title, songci_io.getvalue()

    def _next_word_pattern(self):
        try:
            word_pattern = self._word_patterns.popleft()
        except IndexError as e:
            self.logger.error('Not enough word patterns.')
            raise e
        return word_pattern

    def _analyze(self):
        self._word_patterns = deque()
        verses = sub_verses(self._tune.pattern)
        rhyme = self.rhyme or 'i'
        min_emblem_len = 2
        for verse in verses:
            sub_patterns = list(MapReduceDriver.chunks(verse, min_emblem_len))
            if len(verse) % 2 and len(sub_patterns) >= 2:
                sub_patterns[-2] += sub_patterns[-1]
                sub_patterns.pop()

            self._word_patterns.extend((WordPattern(
                length=len(s), tones_regex=to_tones_regex(s),
                rhyme=rhyme if is_yun(s) else None
            ) for s in sub_patterns))
