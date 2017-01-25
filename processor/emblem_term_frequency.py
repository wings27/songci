import multiprocessing
import operator

from processor.data_source import MongoDataSource
from processor.verse import VerseProcessor


class EmblemTF:
    def __init__(self):
        self._doc_generator = MongoDataSource().document_generator()
        self._tf_stat = {}
        self._lock = multiprocessing.Lock()

    @property
    def tf_stat(self):
        return self._tf_stat

    def calc_tf(self):
        try:
            while True:
                with self._lock:
                    doc = next(self._doc_generator)
                verse_processor = VerseProcessor(doc['content'])
                emblem_cut_result = verse_processor.pre_process().punctuation_cut().emblem_cut().result
                for emblem in emblem_cut_result:
                    self._tf_stat[emblem] = self._tf_stat.get(emblem, 0) + 1
        except StopIteration:
            pass


if __name__ == '__main__':
    tf = EmblemTF()
    tf.calc_tf()
    tf_list = sorted(tf.tf_stat.items(), key=operator.itemgetter(1), reverse=True)
    print(tf_list[0:50])
