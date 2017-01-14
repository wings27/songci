from unittest import TestCase

from processor.importer import MongoImporter


class TestMongoImporter(TestCase):
    def test_import_data(self):
        mongo_importer = MongoImporter()
        print(mongo_importer.import_data())
