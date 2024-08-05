import scrapy
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod
from ..items import EcommerceScraperItem


class EcommerceSpiderSpider(scrapy.Spider):
    name = "ecommerce_spider"
    start_urls = [
        "https://jiji.com.et/cars?filter_attr_100_condition=Brand%20New"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods': [PageMethod("wait_for_timeout", 10)],
                    'errback': self.errback,
                    
                },
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        html_str = await page.content()
        await page.close()

        content = Selector(text=html_str)
        products = content.css("div.masonry-item")

        for product in products:
            product_url = "https://jiji.com.et" +  str(product.css("a").attrib['href'])
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product_data,
            )
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            next_page_url = "https://jiji.com.et" + next_page
            yield response.follow(
                url=next_page_url,
                callback=self.parse,
                meta={
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods': [PageMethod("wait_for_timeout", 10)],
                    'errback': self.errback,
                }
            )

    def parse_product_data(self, response):
        content = response

        prod_item = EcommerceScraperItem()
        prod_item["name"] = content.css("div.b-advert-title-inner.qa-advert-title.b-advert-title-inner--h1::text").get().replace("\n", "").strip()
        prod_item["description"] = ', '.join(desc.strip() for desc in content.css("div.b-advert-attributes__tag::text").getall()).replace("\n", "").strip()
        prod_item["image_urls"] = content.css("img.b-slider-image.qa-carousel-slide::attr('src')").getall()  
        yield prod_item

    async def errback(self, failure):
        page = failure.request.meta["playwright"]
        await page.close()
        self.logger.error('Page closed due to an error: %s', failure)
