# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from .MysqlHelper import MysqlHelper
class SearchspiderPipeline:
    '''
    保存mysql数据库
    '''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_HOST'), mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri, port=27017)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        print('开始处理')
        #print(item)
        title = item['title']
        time = item['time']
        content = item['content']
        url = item['url']
        keyword = item['keyword']

        temple = {
            'title': title,
            'time': time,
            'content': content,
            'url': url,
            'keyword': keyword
        }
        client = pymongo.MongoClient(host="localhost", port=27017)
        # 建库
        db = client.mixmedium
        # 建表
        searchDB = db.search
        coll = db['search']
        if coll.count_documents({'title': title, 'keyword': keyword}) == 0:
            # 存
            insert_id = searchDB.insert_one(temple)
            print(insert_id)
        else:
            print('存在数据')
        return item

    def close_spider(self, spider):
        self.client.close()


