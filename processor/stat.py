import operator

from nlp.emblem import Emblem
from processor.data_source import MongoDataSource

if __name__ == '__main__':
    FREQ_THRESHOLD = 1
    data_source = MongoDataSource()
    emblem = Emblem(data_source.document_generator)
    tf_stat = emblem.emblem_tf()
    tf_list = sorted(tf_stat.items(), key=operator.itemgetter(1), reverse=True)

    total_len = len(tf_list)
    last_count = 0
    last_freq = 0
    for tf_item in tf_list:
        emblem_name, emblem_count = tf_item
        if emblem_count > FREQ_THRESHOLD:
            freq = emblem_count / total_len
            data_source.save_collection('emblem', {'name': emblem_name}, {'$set': {'freq': freq}})
