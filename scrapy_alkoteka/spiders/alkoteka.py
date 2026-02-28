import scrapy
import pathlib
from datetime import datetime


class AlkotekaSpider(scrapy.Spider):
    name = "alkoteka"
    allowed_domains = ["alkoteka.com"]

    CITY_UUID = "4a70f9e0-46ae-11e7-83ff-00155d026416"
    API_URL = "https://alkoteka.com/web-api/v1/product"
    PRODUCT_API_URL = "https://alkoteka.com/web-api/v1/product/{slug}"

    #Наши ссылки
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
            slug = url.rstrip("/").split("/")[-1]
            yield self._make_catalog_request(slug, page=1)

    def _make_catalog_request(self, slug, page):
        url = (
            f"{self.API_URL}"
            f"?city_uuid={self.CITY_UUID}"
            f"&page={page}"
            f"&per_page=20"
            f"&root_category_slug={slug}"
        )
        return scrapy.Request(
            url,
            callback=self.parse_category,
            cb_kwargs={"slug": slug, "page": page},
        )

    def parse_category(self, response, slug, page):
        data = response.json()
        results = data.get("results", [])

        for product in results:
            product_slug = product.get("slug")
            if product_slug:
                full_url = (
                    f"{self.PRODUCT_API_URL.format(slug=product_slug)}"
                    f"?city_uuid={self.CITY_UUID}"
                )
                yield scrapy.Request(
                    full_url,
                    callback=self.parse_product,
                    cb_kwargs={"product_slug": product_slug},
                )

        meta = data.get("meta", {})
        if meta.get("has_more_pages"):
            yield self._make_catalog_request(slug, page + 1)

    def parse_product(self, response, product_slug=""):
        data = response.json().get("results", {})
        timestamp = int(datetime.now().timestamp())

        rpc = str(data.get("vendor_code") or data.get("uuid", ""))

        category_slug = data.get("category", {}).get("slug", "")

        if not product_slug:
            product_slug = data.get("slug", "")

        product_url_from_api = data.get("product_url", "")
        if product_url_from_api:
            url = product_url_from_api
        else:
            url = f"https://alkoteka.com/product/{category_slug}/{product_slug}"

        title = data.get("name", "")
        volume = self._get_label(data, "obem")
        color = self._get_label(data, "cvet")
        if volume and volume not in title:
            title = f"{title}, {volume}"
        elif color and color not in title:
            title = f"{title}, {color}"

        marketing_tags = [
            label.get("title", "")
            for label in data.get("action_labels", [])
            if label.get("title")
        ]
        if data.get("new"):
            marketing_tags.append("Новинка")
        if data.get("recomended"):
            marketing_tags.append("Рекомендуем")

        brand = (
                data.get("brand_name")
                or self._get_label(data, "brand")
                or self._get_label(data, "brend")
                or data.get("country_name", "")
        )

        section = []
        category = data.get("category", {})
        parent = category.get("parent", {})
        if parent.get("name"):
            section.append(parent["name"])
        if category.get("name"):
            section.append(category["name"])

        price_current = float(data.get("price") or 0)
        price_original = float(data.get("prev_price") or price_current)
        sale_tag = ""
        if price_original > price_current and price_original > 0:
            discount = round(100 * (price_original - price_current) / price_original)
            sale_tag = f"Скидка {discount}%"

        price_data = {
            "current": price_current,
            "original": price_original,
            "sale_tag": sale_tag,
        }

        in_stock = data.get("available", False)
        count = data.get("quantity_total", 0)
        stock = {
            "in_stock": bool(in_stock),
            "count": int(count) if count else 0,
        }

        main_image = data.get("image_url", "")
        assets = {
            "main_image": main_image,
            "set_images": [main_image] if main_image else [],
            "view360": [],
            "video": [],
        }

        metadata = {
            "__description": data.get("description") or "",
            "Артикул": str(data.get("vendor_code", "")),
            "Страна": data.get("country_name", ""),
        }
        for label in data.get("filter_labels", []):
            key = label.get("filter", "")
            value = label.get("title", "")
            if key and value:
                metadata[key] = value

        variants = self._count_variants(data)

        yield {
            "timestamp": timestamp,
            "RPC": rpc,
            "url": url,
            "title": title,
            "marketing_tags": marketing_tags,
            "brand": brand,
            "section": section,
            "price_data": price_data,
            "stock": stock,
            "assets": assets,
            "metadata": metadata,
            "variants": variants,
        }

    def _get_label(self, data, filter_name):
        for label in data.get("filter_labels", []):
            if label.get("filter") == filter_name:
                return label.get("title", "")
        return ""

    def _count_variants(self, data):
        volume_labels = [
            l for l in data.get("filter_labels", [])
            if l.get("filter") in ("obem", "cvet")
        ]
        return len(volume_labels) if volume_labels else 1
