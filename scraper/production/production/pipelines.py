# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from utils.calculate import combine_normal_internal
from utils.calculate import refine_tx


class ProductionPipeline:
    def create_tx(self, item):
        return {
            'address': item['address'],
            'category': item['category']
        }

    def open_spider(self, spider):
        self.file = open('data/tx.json', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        tx = self.create_tx(item)
        txlist = []
        txlistinternal = []
        if item['txlist'] is not None:
            for i in item['txlist']:
                txlist.append(refine_tx(i, item['address'], 'txlist'))
        if item['txlistinternal'] is not None:
            for i in item['txlistinternal']:
                txlistinternal.append(refine_tx(i, item['address'], 'txlistinternal'))
        tx['txs'] = combine_normal_internal(txlist, txlistinternal)
        line = json.dumps(tx) + "\n"
        self.file.write(line)
