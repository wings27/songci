from unittest import TestCase

from processor.data_source import MongoDataSource


class TestMongoImporter(TestCase):
    def test_import_data(self):
        mongo_importer = MongoDataSource()
        for document in mongo_importer.document_generator():
            print(document)
