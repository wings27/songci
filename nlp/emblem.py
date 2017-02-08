from nlp.verse import Verse


class Emblem:
    def __init__(self, docs):
        self._docs = docs

    @property
    def result(self):
        return self._docs

    def emblem_tf(self):
        stat = {}
        for doc in self._docs:
            verse_processor = Verse(doc['content'])
            emblem_cut_result = verse_processor.trim_comment().punctuation_cut().emblem_cut().result
            for emblem in emblem_cut_result:
                stat[emblem] = stat.get(emblem, 0) + 1
        return stat
