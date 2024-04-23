
from weibo.items import WeiboItem
from copy import deepcopy
import scrapy
import json
 
class WbSpider(scrapy.Spider):
    name = "wb"
    allowed_domains = ["m.weibo.cn"]
    Q = input('请输入搜索关键词：')
    page = 1
    start_urls = [f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{Q}"  #ah, so it has parsed the url format of weibo, to change it according to our searching/iterating request
                  f"%26t%3D%26page_type=searchall&page={page}"]
 
    #here it mainly handles long-short text problem
    def parse(self, response):
        result = json.loads(response.text)   #json.loads transform raw json data as a string to python dictionary
        result = result['data']['cards']     #extracts the list of cards from the JSON structure, each card will be a post or activity in weibo
        item = WeiboItem()
        for detail in result:
            item['_id'] = detail['mblog']['user']['id']
            item['_name'] = detail['mblog']['user']['screen_name']
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', detail['mblog']['isLongText'])
 
            if detail['mblog']['isLongText'] is True:   #if the mblog is long-text, it means the post is truncated,and the full-text need to be fetched from another URL  
                blog_id = detail['mblog']['id']
                blog_id = ''.join(blog_id)
                full_text_url = 'https://m.weibo.cn/statuses/extend?id=' + blog_id
                yield scrapy.Request(full_text_url, callback=self.long_text_parse, meta={'item': deepcopy(item)},
                                     priority=1)
            else:
                _text = detail['mblog']['text']
                _text = _text.replace('\n', '')
                _text = ''.join([x.strip() for x in _text])
                item['_text'] = _text
                yield item
 
        self.page += 1
        next_page = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{self.Q}" \
                    f"%26t%3D%26page_type=searchall&page={self.page}"
        yield scrapy.Request(next_page, callback=self.parse, meta={'item': item})
 
    def long_text_parse(self, response):
        result = json.loads(response.text)
        item = response.meta['item']
        _text = result['data']['longTextContent']
        _text = _text.replace('\n', '')
        _text = ''.join([x.strip() for x in _text])
        item['_text'] = _text
        yield item