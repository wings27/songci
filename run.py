from processor.emblem_processor import EmblemProcessor
from processor.songci_dao import MongoDAO


def main():
    mongo_dao = MongoDAO()
    processor = EmblemProcessor(mongo_dao)

    mongo_dao.save_emblems_field(processor.gen_freq_rate(), 'freq_rate')
    mongo_dao.save_emblems_field(processor.gen_finals(), 'finals')


if __name__ == '__main__':
    main()
