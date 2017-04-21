import logging
import multiprocessing
from abc import abstractmethod, ABCMeta
from itertools import repeat

import pymongo

from mapreduce.driver import MapReduceDriver
from processor.data_source import MongoDataSource


class AbstractDAO(metaclass=ABCMeta):
    @abstractmethod
    def load_songci_contents(self):
        pass

    @abstractmethod
    def load_emblem_names(self):
        pass

    @abstractmethod
    def save_emblems_field(self, emblem_with_field_list, field_name, index):
        """
        Save emblems along with provided field,
        where field can be any of the types that self.data_source supports.
    
        :param emblem_with_field_list: tuple of (emblem_name, field)
        :param field_name: the name of that field
        :param index: whether to create an index on the field.
    
        :return: None
        """
        pass


class MongoDAO(AbstractDAO):
    COLLECTION_EMBLEM = 'emblem'
    COLLECTION_SONGCI_CONTENT = 'songci_content'

    logger = logging.getLogger('processor.MongoDAO')
    logging.basicConfig(level=logging.INFO)

    data_source = MongoDataSource()

    def load_songci_contents(self):
        return [songci['content'] for songci in (self.data_source.find(
            self.COLLECTION_SONGCI_CONTENT))]

    def load_emblem_names(self):
        return [emblem['name'] for emblem in (self.data_source.find(
            self.COLLECTION_EMBLEM,
            projection=['name'], sort=[('freq_rate', pymongo.DESCENDING)]))]

    def random_emblem_name(self, where=None, size=1):
        pipeline = [
            {"$match": where},
            {"$sample": {"size": size}},
            {"$project": {"name": "$name"}},
        ]
        return self.data_source.aggregate(self.COLLECTION_EMBLEM, pipeline)

    def save_emblems_field(
            self, emblem_with_field_list, field_name, index=True):
        total_len = len(emblem_with_field_list)
        self.logger.info('Saving field [%s], total=%d', field_name, total_len)

        workers = (multiprocessing.cpu_count() or 1)
        emblem_freq_chunks = MapReduceDriver.chunks(
            emblem_with_field_list, int(total_len / workers))

        if index:
            self.data_source.create_index(
                self.COLLECTION_EMBLEM, 'name', unique=True)
            self.data_source.create_index(
                self.COLLECTION_EMBLEM, field_name)
            field = emblem_with_field_list[0][1]
            if isinstance(field, dict):
                for key in field.keys():
                    self.data_source.create_index(
                        self.COLLECTION_EMBLEM, field_name + '.' + key)

        with multiprocessing.Pool(processes=workers) as pool:
            pool.starmap(
                self._save_emblems_field,
                zip(emblem_freq_chunks, repeat(field_name)))

    def _save_emblems_field(self, emblem_with_field_list, field_name):
        self.data_source.save_many(
            self.COLLECTION_EMBLEM,
            [({'name': name}, {field_name: field})
             for (name, field) in emblem_with_field_list])
