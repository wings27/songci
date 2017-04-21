from nlp.pinyin import finals_info


class EmblemFinals:
    @staticmethod
    def map_fn(item_list):
        return [(item, finals_info(item)) for item in item_list]

    @staticmethod
    def reduce_fn(item_mapping):
        item_key, item_values = item_mapping
        return item_key, item_values[0]
