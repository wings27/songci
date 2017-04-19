import logging

from processor.emblem_processor import EmblemProcessor
from processor.songci_dao import MongoDAO
from writer.songci_writer import SongciWriter


def main():
    mongo_dao = MongoDAO()
    processor = EmblemProcessor(mongo_dao)

    mongo_dao.save_emblems_field(processor.gen_freq_rate(), 'freq_rate')
    mongo_dao.save_emblems_field(processor.gen_finals(), 'finals')

    songci_writer = SongciWriter(
        tune_name='huanxisha', rhyme='an', data_source_dao=mongo_dao)
    for i in range(5):
        title, content = songci_writer.write_new()
        print('\n《%s》\n\n%s\n\n' % (title, content))


if __name__ == '__main__':
    main()
