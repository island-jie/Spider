# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class SearchspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
    百家号item
    '''
    collection = 'search'
    keyword = Field()
    content = Field()
    title = Field()
    time = Field()
    url = Field()
