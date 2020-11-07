import scrapy
import urllib.parse
import requests
import re
import datetime
from ..items import SearchspiderItem
import pymongo
import hashlib
import os
import pickle
import logging
import requests

from gne import GeneralNewsExtractor

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['baidu.com']
    #start_urls = ['http://baidu.com/']
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/61.0.3163.79 Safari/537.36",
    }
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': header,
        'DOWNLOAD_DELAY': 0.5,
        'DOWNLOADER_MIDDLEWARES': {
            # 'baiduCrawler.middlewares.BaiducrawlerDownloaderMiddleware': 543,
        },
        'MONGO_HOST': 'localhost',
        'MONGO_PORT': 27017,
        'MONGO_DB': 'search',
        'ITEM_PIPELINES': {
            'searchSpider.pipelines.SearchspiderPipeline': 300,
        }
    }
    mongo_host = custom_settings['MONGO_HOST']
    mongo_port = custom_settings['MONGO_PORT']
    mongo_db = custom_settings['MONGO_DB']
    client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
    db = client[mongo_db]

    base_url = 'https://www.baidu.com/s?medium=2&tn=news&word={}&pn={}'
    # 更新的新闻数量
    new_news = 0

    def __init__(self, keywords=None, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.keys = keywords.split(',')

    def baijiahao_log(self):
        '''
        logger函数，在文件和控制台输出信息
        :return:
        '''
        # 创建logger，如果参数为空则返回root logger
        logger = logging.getLogger("baijiahaoLogger")
        logger.setLevel(logging.DEBUG)  # 设置logger日志等级​
        # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        if not logger.handlers:
            # 创建handler
            fh = logging.FileHandler("baijiahaolog.log", encoding="utf-8")
            ch = logging.StreamHandler()
            # 设置输出日志格式
            formatter = logging.Formatter(
                fmt="%(asctime)s %(name)s %(filename)s %(message)s",
                datefmt="%Y/%m/%d %X"
            )
            # 为handler指定输出格式
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            # 为logger添加的日志处理器
            logger.addHandler(fh)
            logger.addHandler(ch)
        return logger  # 直接返回logger

    def start_requests(self):
        logger = self.baijiahao_log()
        logger.info(
            '---------------------------------baijiahao Spider started {}----------------------------------------'.format(
                datetime.date.today().strftime('%Y-%m-%d')
            )
        )
        # start_urls= []
        for key in self.keys:
            url = self.base_url.format(urllib.parse.quote(key), 0)
            print(url)
            yield scrapy.Request(
                url = url,
                dont_filter = True,
                meta={"keyword": key},
                callback = self.parse_post,
            )
    def parse(self,response):
        """
        默认是get请求，卡了一晚上！！！！！！！！！！
        :param response:
        :return:
        """
        pass

    def parse_post(self, response):
        '''
        对爬取到的百度页面进行解析，获得百家号的链接
        如果未爬取到百度的检索结果，则重新请求百度链接
        :param response:
        :return:
        '''
        print(response)
        #logger = self.baijiahao_log()
        key = response.meta.get('keyword')
        print(key)
        #logger.info("【{}】【start url】:{}".format(key, response.url))
        #获取下一页
        next_page = response.xpath('//a[@class="n"][text()="下一页 >"]/@href').get()
        if next_page:
            #print(next_page)
            #拼接网址
            next_url = 'https://www.baidu.com' + next_page
            print('下一页地址是：')
            #next_url = response.urljion(next_page)
            print(next_url)
            #发出请求 Request；callback是回调函数，将请求得到的相应交给自己处理
            yield scrapy.Request(
                url=next_url,
                dont_filter=True,
                meta={"keyword": key},
                callback=self.parse_post,
            )
        #获取这一页的所有（10条）新闻
        hrefs = response.xpath('//h3[@class="news-title_1YtI1"]/a/@href').extract()
        print("本页10条内容")
        print(hrefs)
        for href in hrefs:
            yield scrapy.Request(href,
                                 dont_filter=True,
                                 meta={"keyword": key},
                                 callback=self.parse_baijiahao
                                 )

    def parse_baijiahao(self, response):
        extractor = GeneralNewsExtractor()
        result = extractor.extract(response.text)
        #print(result)
        title = result['title']
        time = result['publish_time']
        content = result['content']
        url = response.url
        keyword = response.meta.get('keyword')
        items = {
            'title': title,
            'time': time,
            'content': content,
            'url':url,
            'keyword':keyword
        }
        yield items
