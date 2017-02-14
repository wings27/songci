import pypinyin
from pypinyin import pinyin


def finals_tone(word):
    return pinyin(word, style=pypinyin.FINALS_TONE3)
