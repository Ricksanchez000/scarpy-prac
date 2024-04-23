# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import json

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class WeiboSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class WeiboDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    
    #newly added
    def __init__(self):
        self.cookies = None
    
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    #newly added
    def spider_opened(self, spider):

        try:
            with open('cookies.txt', 'r') as f:
                raw_cookies = json.load(f)
                self.cookies = {cookie['name']: cookie['value'] for cookie in raw_cookies}
                self.cookies_loaded = True
                spider.logger.info("Cookies loaded successfully.")
        except Exception as e:
            spider.logger.error(f"Failed to load cookies: {e}")
            self.cookies_loaded = False

        '''
        with open('cookies.txt', 'r') as f:
            self.cookies = json.load(f)
        spider.logger.info(f"Loaded cookies: {self.cookies}")
        '''
    
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        
        if not self.cookies:
            spider.logger.warning("Attempting to load cookies again.")
            self.spider_opened(spider)

        if self.cookies:
            request.cookies = self.cookies
            request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            spider.logger.debug(f"Cookies set for request {request.url}: {request.cookies}")
        else:
            spider.logger.warning("Cookies were not loaded, sending request without cookies")
            
        
        '''
        
        if self.cookies:
            # Apply cookies to each request
            request.cookies = self.cookies
            request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'
        else:
            spider.logger.warning("Cookies not loaded, please check the 'cookies.txt' file.")
        '''   
           
        '''
        request.headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'}
        with open('cookies.txt', 'r') as f:
            cookies = json.load(f)
            request.cookies = cookies
        '''

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
