from nlp.verse import Verse


class Emblem:
    def __init__(self, docs):
        self._docs = docs

    @property
    def result(self):
        return self._docs

    def emblem_term_freq(self):
        stat = {}
        for doc in self._docs:
            verse = Verse(doc['content'])
            emblem_cut_result = verse.emblem_cut()
            for emblem in emblem_cut_result:
                stat[emblem] = stat.get(emblem, 0) + 1
        return stat
