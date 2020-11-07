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
    def process_item(self, item, spider):
        #对传过来的数据进行处理
        print("kkkkkkkkkkkkkkkkkkkkkk")
        #print(item)
        title = item['title']
        time = item['time']
        content = item['content']
        url = item['url']
        keyword = item['keyword']
        localhost = "127.0.0.1"
        port = 27017
        temple ={
            'title':title,
            'time':time,
            'content':content,
            'url':url,
            'keyword':keyword
        }
        # 连接数据库
        client = pymongo.MongoClient(host="localhost", port=port)
        # 建库
        db = client.mixmedium
        # 建表
        searchDB = db.search
        # 存
        insert_id = searchDB.insert_one(temple)
        print(insert_id)
        #mysql有点问题
        # msh = MysqlHelper.MysqlHelper(host="localhost",port=3306, username="root", password="123456", db="mixmedium",
        #                               charset="utf8")
        # msh.connect()
        # sql = "insert into baidu_search_news values('{}','{}','{}','{}','{}')".format(
        #    content, time, title, url, keyword)
        # print(sql)
        # msh.insert(sql)
        return item
    def close_spider(self,spider):
        #self.f.close()
        print("爬取完毕")
        spider.crawler.engine.close_spider(spider, '没有新数据关闭爬虫')


