import itertools

from nlp.pinyin import finals_tone


class EmblemFinals:
    @staticmethod
    def map_fn(item_list):
        return [(item, tuple(itertools.chain.from_iterable(finals_tone(item)))) for item in item_list]

    @staticmethod
    def reduce_fn(item_mapping):
        item_key, item_values = item_mapping
        return item_key, tuple(sorted(item_values))
