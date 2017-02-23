import logging

import jieba
import pypinyin
from pypinyin import pinyin

jieba.setLogLevel(logging.WARNING)


def finals_tone(word):
    return pinyin(word, style=pypinyin.FINALS_TONE3)
