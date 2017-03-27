from nlp.verse import Verse


class Emblem:
    def __init__(self, songci_list):
        self._songci_list = songci_list
        self._emblem_list = None

    def raw_emblem_list(self):
        if self._emblem_list is None:
            ret = []
            for songci in self._songci_list:
                verse = Verse(songci)
                ret.extend(verse.emblem_cut())
            self._emblem_list = ret
        return self._emblem_list
