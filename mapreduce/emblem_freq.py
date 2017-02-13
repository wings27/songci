class EmblemFreq:
    def __init__(self, emblems):
        self._emblems = emblems

    @staticmethod
    def map_fn(item_list):
        return [(item, 1) for item in item_list]

    @staticmethod
    def reduce_fn(item_mapping):
        item_key, item_values = item_mapping
        return item_key, sum(item_values)
