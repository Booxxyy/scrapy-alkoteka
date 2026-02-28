# alkoteka-parser

Парсер товаров интернет-магазина [alkoteka.com](https://alkoteka.com) на базе **Scrapy**.
Реализован без использования Playwright, Selenium и Headless-браузеров — только нативный Scrapy.

---

## Функциональность

- Обход каталога по списку категорий с автоматической пагинацией (`has_more_pages`)
- Сбор данных о товарах: цены, остатки, изображения, характеристики, маркетинговые теги
- Учёт региона — цены и наличие актуальны для **Краснодара** (`city_uuid`)
- Поддержка прокси через кастомный `ProxyMiddleware`
- Учёт региона через `RegionMiddleware` (cookie-заголовки)
- Два варианта задания входных категорий: константа в коде или внешний файл
- Сохранение результата в `result.json` в соответствии с заданным форматом

---

## Стек технологий

- Python 3.11+
- Scrapy 2.x
- JSON API alkoteka.com (без HTML-парсинга)

Установка зависимостей:

```bash
pip install -r requirements.txt
```

---

## Запуск

```bash
scrapy crawl alkoteka -O result.json
```

С указанием файла категорий:

```bash
scrapy crawl alkoteka -a urls_file=urls.txt -O result.json
```

---

## Входные данные

Два варианта задать список категорий:

**Вариант 1** — константа в `spiders/alkoteka.py`:

```python
START_URLS = [
    "https://alkoteka.com/catalog/vino",
    "https://alkoteka.com/catalog/krepkiy-alkogol",
    "https://alkoteka.com/catalog/produkty-1",
]
```

**Вариант 2** — текстовый файл, одна ссылка на строку:

```
https://alkoteka.com/catalog/vino
https://alkoteka.com/catalog/krepkiy-alkogol
https://alkoteka.com/catalog/slaboalkogolnye-napitki-2
```

---

## Выходные данные

Каждый товар сохраняется в `result.json` по следующему формату:

```json
{
  "timestamp": 1740000000,
  "RPC": "130687",
  "url": "https://alkoteka.com/product/chay-kofe-1/kimbo-espresso-napoletano_130687",
  "title": "Kimbo Espresso Napoletano, кофе мол. жб 250 гр",
  "marketing_tags": ["Скидка"],
  "brand": "Kimbo",
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
    "categories": "Чай, кофе"
  },
  "variants": 1
}
```

## Настройки (`settings.py`)

| Параметр | Описание |
|---|---|
| `CITY_UUID` | UUID региона Краснодар — подставляется в каждый API-запрос |
| `REGION_COOKIES` | Cookie-заголовки для привязки к региону |
| `PROXY_LIST` | Список прокси `http://user:pass@host:port` |
| `DOWNLOAD_DELAY` | Задержка между запросами (сек) |
| `CLOSESPIDER_ITEMCOUNT` | Лимит товаров для тестового прогона (убрать при полном сборе) |

### Прокси

```python
PROXY_LIST = [
    "http://user:password@host1:port",
    "http://user:password@host2:port",
]
```

При каждом запросе случайно выбирается прокси из списка через `ProxyMiddleware`.
Если список пуст — запросы идут напрямую.

---

## Архитектура

```
scrapy_alkoteka/
├── spiders/
│   └── alkoteka.py       # Основной паук: обход каталога + парсинг карточек
├── middlewares.py         # RegionMiddleware + ProxyMiddleware
├── settings.py            # Конфигурация проекта
└── items.py
```

### Middleware

- **RegionMiddleware** — подставляет куки из `REGION_COOKIES` в каждый запрос
- **ProxyMiddleware** — рандомно выбирает прокси из `PROXY_LIST` и применяет к запросу

---

## Ожидаемый результат

После запуска паука в корне проекта появится файл `result.json` со списком товаров
по всем заданным категориям в установленном формате.

```bash
scrapy crawl alkoteka -O result.json
```
