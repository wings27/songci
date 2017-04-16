import logging
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

    def fetch_word(self) -> (str, int):
        # todo fetch word by word_pattern
        return self.tones_regex, self.length


class SongciWriter:
    logger = logging.getLogger('processor.EmblemProcessor')
    logging.basicConfig(level=logging.INFO)

    def __init__(self, tune_name, rhyme) -> None:
        self.tune_name = tune_name
        self.rhyme = rhyme

        self._tune = load_tune(self.tune_name)
        self._word_patterns = None
        self._write_pointer = None

    def write_new(self) -> (str, str):
        if not self._tune.pattern:
            raise ValueError(
                'pattern for tune [%s] is empty.' % self.tune_name)
        pattern = self._tune.pattern

        self._analyze()

        with StringIO() as songci_io:
            self._write_pointer = 0
            while self._write_pointer < len(pattern):
                char = pattern[self._write_pointer]
                if char in pingze.ping_ze_chars.values():
                    word, pointer_step = self._next_word_pattern().fetch_word()
                else:
                    word, pointer_step = char, len(char)
                self._write_pointer += pointer_step
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
            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=3, tones_regex='.(3|4)(1|2)', rhyme=rhyme),
            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=3, tones_regex='.(3|4)(1|2)', rhyme=rhyme),

            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=3, tones_regex='.(3|4)(1|2)', rhyme=rhyme),
            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=3, tones_regex='.(3|4)(1|2)', rhyme=rhyme),
            WordPattern(length=2, tones_regex='.(3|4)'),
            WordPattern(length=2, tones_regex='.(1|2)'),
            WordPattern(length=3, tones_regex='.(3|4)(1|2)', rhyme=rhyme),
        ])


if __name__ == '__main__':
    songci_writer = SongciWriter(tune_name='huanxisha', rhyme='ang')
    title, content = songci_writer.write_new()
    print('new_songci: \n《%s》\n\n%s' % (title, content))
