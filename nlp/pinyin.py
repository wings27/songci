import logging
from collections import namedtuple

import jieba
import pypinyin
from pypinyin import pinyin

Finals = namedtuple('Finals', ['pinyin', 'rhyme', 'tones'])
jieba.setLogLevel(logging.WARNING)


def finals_info(word):
    word_pinyin = pinyin(word, style=pypinyin.FINALS_TONE3)
    word_pinyin = tuple(pinyin_list[0] for pinyin_list in word_pinyin)

    word_finals_tone = Finals(pinyin=word_pinyin,
                              rhyme=word_pinyin[-1][:-1],
                              tones=''.join((char_pinyin[-1]
                                             for char_pinyin in word_pinyin)))
    return word_finals_tone
