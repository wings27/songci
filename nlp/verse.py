import re

re_comment = re.compile(r'\(.+?\)')
re_punctuation_list = re.compile(
    r'\s+|,|!|:|;|\(|\)|，|。|？|！|…|：|；|、|‘|’|“|”|（|）|《|》')


def emblem_cut(verse, lengths=(2, 3)):
    subs = sub_verses(verse)
    result = []
    for length in lengths:
        for sub in subs:
            for i in range(len(sub) - (length - 1)):
                result.append(sub[i:i + length])
    return result


def sub_verses(verse):
    verse = _trim_comment(verse)
    return _punctuation_cut(verse)


def _trim_comment(verse):
    ret = re_comment.sub('', verse)
    return ret


def _punctuation_cut(verse):
    list_split = re_punctuation_list.split(verse)
    ret = list(filter(None, list_split))

    return ret
