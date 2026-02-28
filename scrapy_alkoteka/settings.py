BOT_NAME = "scrapy_alkoteka"

SPIDER_MODULES = ["scrapy_alkoteka.spiders"]
NEWSPIDER_MODULE = "scrapy_alkoteka.spiders"

ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
}

# Регион
REGION_NAME = "Краснодар"
REGION_COOKIES = {
    # Заполнить
}

# Прокси
PROXY_LIST = [
    # Заполнить
]

DOWNLOADER_MIDDLEWARES = {
    "scrapy_alkoteka.middlewares.RegionMiddleware": 543,
    "scrapy_alkoteka.middlewares.ProxyMiddleware": 544,
}

DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
AUTOTHROTTLE_ENABLED = True

LOG_LEVEL = "INFO"
