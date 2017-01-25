import re


class VerseProcessor:
    _punctuation_list = re.compile('\\n+|,|!|:|;|\(|\)|，|。|？|！|…|：|；|、|‘|’|“|”|（|）')
    _comment = re.compile('\\(.+?\\)')

    def __init__(self, verse_list):
        if isinstance(verse_list, str):
            verse_list = [verse_list]
        self._verse_list = verse_list

    @property
    def result(self):
        return self._verse_list

    def pre_process(self):
        result = []
        for verse in self._verse_list:
            result.append(self._comment.sub('', verse))
        self._verse_list = result
        return self

    def punctuation_cut(self):
        result = []
        for verse in self._verse_list:
            list_split = self._punctuation_list.split(verse)
            result.extend(list(filter(None, list_split)))
        self._verse_list = result
        return self

    def emblem_cut(self, lengths=(2, 3)):
        result = []
        for length in lengths:
            for verse in self._verse_list:
                for i in range(len(verse) - (length - 1)):
                    result.append(verse[i:i + length])
        self._verse_list = result
        return self
