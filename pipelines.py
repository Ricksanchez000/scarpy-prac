# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from weibo.spiders.wb import WbSpider
from itemadapter import ItemAdapter
import csv

"""

class WeiboPipeline:
    def __init__(self):
        self.file = None
        self.writer = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        self.file = open(f'{spider.Q}.csv', 'w', encoding='utf8', newline='')
        fieldnames = ['_id', '_name', '_text']
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(dict(item))
        return item
    """

class WeiboPipeline:    
    def __init__(self):
        self.f = open(f'{WbSpider.Q}.csv', 'w', encoding='utf8', newline='')
        self.file_name = ['_id', '_name', '_text']
        self.writer = csv.DictWriter(self.f, fieldnames=self.file_name)
        self.writer.writeheader()
 
    def process_item(self, item, spider):
        self.writer.writerow(dict(item))
        return item
 
    def close_spider(self, spider):
        self.f.close()
    