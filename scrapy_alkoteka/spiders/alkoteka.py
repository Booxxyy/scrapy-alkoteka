import scrapy
import pathlib
from datetime import datetime

class AlkotekaSpider(scrapy.Spider):
    name = "alkoteka"
    allowed_domains = ["alkoteka.com"]

    # Ссылки
    START_URLS = [
        "https://alkoteka.com/catalog/produkty-1",
        "https://alkoteka.com/catalog/krepkiy-alkogol",
        "https://alkoteka.com/catalog/vino",
    ]

    def __init__(self, urls_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls_from_file = []
        if urls_file:
            path = pathlib.Path(urls_file)
            if path.exists():
                with path.open("r", encoding="utf-8") as f:
                    for line in f:
                        url = line.strip()
                        if url:
                            self.urls_from_file.append(url)

    def start_requests(self):
        start_urls = self.urls_from_file or self.START_URLS
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse_category)

    def parse_category(self, response):
        pass # Дописать

    def parse_product(self, response, category_url=""):
        pass # Дописать