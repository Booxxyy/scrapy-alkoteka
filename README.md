```markdown
Парсер на Scrapy для сбора товаров с сайта https://alkoteka.com.

Особенности:
- Работает напрямую с JSON API сайта (без HTML-парсинга)
- Учитывает регион — цены и наличие актуальны для *Краснодара*
- Поддержка прокси через middleware
- Вход — список ссылок на категории (константа или файл)

---

## Быстрый старт

```bash
git clone https://github.com/Booxxyy/scrapy-alkoteka.git
cd scrapy-alkoteka
pip install -r requirements.txt
scrapy crawl alkoteka -O result.json
```

---

## Входные данные

Два варианта задать категории:

**Вариант 1** — константа в `spiders/alkoteka.py`:
```python
START_URLS = [
    "https://alkoteka.com/catalog/vino",
    "https://alkoteka.com/catalog/krepkiy-alkogol",
    "https://alkoteka.com/catalog/produkty-1",
]
```

**Вариант 2** — текстовый файл, одна ссылка на строку:
```bash
scrapy crawl alkoteka -a urls_file=urls.txt -O result.json
```

---

## Конфигурация

Все параметры в `scrapy_alkoteka/settings.py`:

```python
# Куки региона Краснодар (опционально, тк регион уже задан через CITY_UUID в пауке)
REGION_COOKIES = {}

# Список прокси
PROXY_LIST = [
    # "http://user:password@host:port",
]

# Задержка между запросами
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# Лимит для тестового прогона (убрать для полного сбора)
# CLOSESPIDER_ITEMCOUNT = 50
```
---

## Формат выходных данных

```json
{
  "timestamp": 1740000000,
  "RPC": "130687",
  "url": "https://alkoteka.com/product/chay-kofe-1/kimbo-espresso-napoletano_130687",
  "title": "Kimbo espresso napoletano, кофе мол. жб 250 гр",
  "marketing_tags": ["Скидка"],
  "brand": "Италия",
  "section": ["Продукты", "Чай, кофе"],
  "price_data": {
    "current": 990.0,
    "original": 1350.0,
    "sale_tag": "Скидка 27%"
  },
  "stock": {
    "in_stock": true,
    "count": 220
  },
  "assets": {
    "main_image": "https://web.alkoteka.com/storage/product/12/27/130687_image.png",
    "set_images": ["https://web.alkoteka.com/storage/product/12/27/130687_image.png"],
    "view360": [],
    "video": []
  },
  "metadata": {
    "__description": "",
    "Артикул": "130687",
    "Страна": "Италия",
    "categories": "Чай, кофе",
    "strana": "Италия"
  },
  "variants": 1
}
```

---

## Middleware

### RegionMiddleware
Подставляет куки региона из `REGION_COOKIES` в каждый запрос. Регион Краснодар дополнительно
задан жёстко через `CITY_UUID` в пауке — цены и наличие соответствуют выбранному региону.

### ProxyMiddleware
На каждый запрос случайно выбирает прокси из `PROXY_LIST`. Если список пустой — запросы
идут напрямую без прокси.
```