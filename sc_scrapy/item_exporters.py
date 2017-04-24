from scrapy.contrib.exporter import JsonItemExporter, JsonLinesItemExporter


class UnicodeJsonItemExporter(JsonItemExporter):
    def __init__(self, file, **kwargs):
        super().__init__(file, ensure_ascii=False, **kwargs)


class UnicodeJsonLinesItemExporter(JsonLinesItemExporter):
    def __init__(self, file, **kwargs):
        super().__init__(file, ensure_ascii=False, **kwargs)
