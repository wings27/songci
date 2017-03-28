import re


class Verse:
    def __init__(self, verses):
        if isinstance(verses, str):
            verses = [verses]
        self._verses = verses
        self._pre_processed = False

    def emblem_cut(self, lengths=(2, 3)):
        self._pre_process()
        result = []
        for length in lengths:
            for verse in self._verses:
                for i in range(len(verse) - (length - 1)):
                    result.append(verse[i:i + length])
        return result

    def _pre_process(self):
        if not self._pre_processed:
            self._trim_comment()._punctuation_cut()
            self._pre_processed = True

    def _trim_comment(self):
        re_comment = re.compile(r'\(.+?\)')
        result = []
        for verse in self._verses:
            result.append(re_comment.sub('', verse))
        self._verses = result
        return self

    def _punctuation_cut(self):
        re_punctuation_list = re.compile(
            r'\n+|,|!|:|;|\(|\)|，|。|？|！|…|：|；|、|‘|’|“|”|（|）|《|》')
        result = []
        for verse in self._verses:
            list_split = re_punctuation_list.split(verse)
            result.extend(list(filter(None, list_split)))
        self._verses = result
        return self
