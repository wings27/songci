import operator

from nlp.emblem import Emblem
from processor.data_source import MongoDataSource

data_source = MongoDataSource()
emblem = Emblem(data_source.document_generator)


def stat_emblem_tf():
    count_threshold = 1
    tf = emblem.emblem_term_freq()
    tf_sorted = sorted(tf.items(), key=operator.itemgetter(1), reverse=True)
    total_len = len(tf_sorted)

    prev_count = prev_freq = 0  # cache previous quotient (a.k.a. freq) to improve performance
    for tf_item in tf_sorted:  # todo: optimize this using concurrency
        emblem_name, count = tf_item
        if count <= count_threshold:
            break
        freq = prev_freq if count == prev_count else count / total_len
        data_source.save_to_collection('emblem', {'name': emblem_name}, {'freq': freq})
        prev_count = count
        prev_freq = freq
    data_source.create_index('emblem', 'name', unique=True)
    data_source.create_index('emblem', 'freq')


if __name__ == '__main__':
    stat_emblem_tf()
