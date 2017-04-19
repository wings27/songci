import logging
import re
from collections import deque
from io import StringIO

from nlp import pingze
from nlp.verse import sub_verses
from tune_data import load_tune


class WordPattern:
    def __init__(self, length, tones_regex, rhyme=None) -> None:
        self.length = length
        self.tones_regex = tones_regex
        self.rhyme = rhyme

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

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
        pattern = self._tune.pattern

        self._analyze()

        with StringIO() as songci_io:
            pointer = 0
            while pointer < len(pattern):
                char = pattern[pointer]
                if char in pingze.ping_ze_chars.values():
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
        verses = sub_verses(self._tune.pattern)
        print('verses: %s' % verses)
        # todo complete me
        rhyme = self.rhyme or 'i'
        self._word_patterns = deque([
            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=3, tones_regex='.(3|4)(1|2)', rhyme=rhyme),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=3, tones_regex='(3|4)(1|2)(1|2)', rhyme=rhyme),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=3, tones_regex='(3|4)(1|2)(1|2)', rhyme=rhyme),

            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=3, tones_regex='(1|2)(3|4)(3|4)'),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=3, tones_regex='(3|4)(1|2)(1|2)', rhyme=rhyme),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=3, tones_regex='(3|4)(1|2)(1|2)', rhyme=rhyme),
        ])


if __name__ == '__main__':
    songci_writer = SongciWriter(tune_name='huanxisha', rhyme='an')
    title, content = songci_writer.write_new()
    print('new_songci: \n《%s》\n\n%s' % (title, content))
