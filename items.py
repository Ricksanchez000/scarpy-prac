# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#so, here we just somehow build a container to contain our crawled data, but we have already set proper format of this container to save our wanted information 

class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    _name = scrapy.Field()
    _text = scrapy.Field()
    
