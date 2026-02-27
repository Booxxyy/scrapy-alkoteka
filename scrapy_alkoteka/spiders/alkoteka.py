import scrapy


class AlkotekaSpider(scrapy.Spider):
    name = "alkoteka"
    allowed_domains = ["alkoteka.com"]
    start_urls = ["https://alkoteka.com"]

    def parse(self, response):
        pass
