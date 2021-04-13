import os
import csv
from itemadapter import ItemAdapter

class CsvPipeline(object):
    def __init__(self, csv_root_path):
        self.store_file_config = {}
        self.store_file_spider_config = {}
        self.csv_root_path = csv_root_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            csv_root_path=crawler.settings.get('CSV_ROOT_PATH', os.path.dirname(__file__))
        )

    def create_or_find(self, spider, item):
        if self.store_file_config.get(item.csv_meta['name'], None):
            return self.store_file_config[item.csv_meta['name']]

        store_file = '{}/{}.csv'.format(self.csv_root_path, item.csv_meta['name'])
        file = open(store_file, 'a+', encoding="utf-8", newline='')
        writer = csv.writer(file, dialect="excel")
        config = {
            'writer': writer,
            'file': file
        }
        self.store_file_config[spider.name] = config
        self.store_file_spider_config.setdefault(spider.name, [])
        self.store_file_spider_config[spider.name].append(config)
        config['writer'].writerow(item.csv_meta['keys'])
        return config

    def process_item(self, item, spider):
        config = self.create_or_find(spider, item)
        config['writer'].writerow(item.to_csv_row())
        return item

    def close_spider(self, spider):
        for config in self.store_file_spider_config[spider.name]:
            config['file'].close()
