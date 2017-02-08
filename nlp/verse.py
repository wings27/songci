import re


class Verse:

    def __init__(self, verse_list):
        if isinstance(verse_list, str):
            verse_list = [verse_list]
        self._result = verse_list

    @property
    def result(self):
        return self._result

    def trim_comment(self):
        re_comment = re.compile('\\(.+?\\)')
        result = []
        for verse in self._result:
            result.append(re_comment.sub('', verse))
        self._result = result
        return self

    def punctuation_cut(self):
        re_punctuation_list = re.compile('\\n+|,|!|:|;|\(|\)|，|。|？|！|…|：|；|、|‘|’|“|”|（|）|《|》')
        result = []
        for verse in self._result:
            list_split = re_punctuation_list.split(verse)
            result.extend(list(filter(None, list_split)))
        self._result = result
        return self

    def emblem_cut(self, lengths=(2, 3)):
        result = []
        for length in lengths:
            for verse in self._result:
                for i in range(len(verse) - (length - 1)):
                    result.append(verse[i:i + length])
        self._result = result
        return self
