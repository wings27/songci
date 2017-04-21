from unittest import TestCase

from nlp.verse import emblem_cut


class TestNlp(TestCase):
    def test_all(self):
        verse = '春花秋月何时了？往事知多少。小楼昨夜又东风，故国不堪回首月明中。\n' \
                 '雕栏玉砌应犹在，只是朱颜改。问君能有几多愁？恰似一江春水向东流。\n' \
                 '(雕 通：阑)'
        print(emblem_cut(verse))
