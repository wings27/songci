import sys

from processor.emblem_processor import EmblemProcessor
from processor.songci_dao import MongoDAO
from writer.songci_writer import SongciWriter


def main(argv):
    mongo_dao = MongoDAO()

    if 'analyse' in argv:
        processor = EmblemProcessor(mongo_dao)

        mongo_dao.save_emblems_field(processor.gen_freq_rate(), 'freq_rate')
        mongo_dao.save_emblems_field(processor.gen_finals(), 'finals')

    if 'write' in argv:
        songci_writer = SongciWriter(
            tune_name='huanxisha', rhyme='ang', data_source_dao=mongo_dao)
        for i in range(5):
            title, content = songci_writer.write_new()
            print('\n《%s》\n\n%s\n\n' % (title, content))


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) <= 1:
        argv.extend(['analyse', 'write'])
    main(argv)
