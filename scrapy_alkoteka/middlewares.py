import random


class RegionMiddleware(object):

    def __init__(self,region_cookies):
        self.region_cookies = region_cookies

    @classmethod
    def from_crawler(cls, crawler):
        region_cookies = crawler.settings.get('REGION_COOKIES', {})
        return cls(region_cookies=region_cookies)

    def process_request(self,request,spider):
        if self.region_cookies:
            request.cookies.update(self.region_cookies)

class ProxyMiddleware:

    def __init__(self, proxies):
        self.proxies = proxies

    @classmethod
    def from_crawler(cls, crawler):
        proxies = crawler.settings.get('PROXY_LIST', [])
        return cls(proxies=proxies)

    def process_request(self,request,spider):
        if not self.proxies:
            return
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy
        spider.logger.debug(f"Используется прокси: {proxy}")
