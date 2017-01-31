import operator

from nlp.verse import Verse
from processor.data_source import MongoDataSource


def emblem_tf(docs):
    stat = {}
    for doc in docs:
        verse_processor = Verse(doc['content'])
        emblem_cut_result = verse_processor.trim_comment().punctuation_cut().emblem_cut().result
        for emblem in emblem_cut_result:
            stat[emblem] = stat.get(emblem, 0) + 1
    return stat


if __name__ == '__main__':
    tf_stat = emblem_tf(MongoDataSource().document_generator)
    tf_list = sorted(tf_stat.items(), key=operator.itemgetter(1), reverse=True)
    print(tf_list[0:50])
