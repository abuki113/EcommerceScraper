import scrapy
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod
import asyncio

class EcommerceSpiderSpider(scrapy.Spider):
    name = "ecommerce_spider"
    url = "https://jiji.com.et/cars?filter_attr_100_condition=Brand%20New"
    def start_requests(self):
       yield scrapy.Request(url=self.url,
                            callback=self.parse,
                            meta=dict(
                                playwright=True,
                                playwright_include_page=True,
                                playwright_page_methods=[
                                    PageMethod("wait_for_timeout", 10),
                                    ],
                                errback=self.errback,
                            )
                             )


    async def parse(self, response):
        page = response.meta["playwright_page"]

        await asyncio.sleep(10)
        html_str = await page.content()            
        await page.close()
        content = Selector(text=html_str)
        products = content.css("div.masonry-item")
        for product in products:
            yield {
                'name': product.css("div.b-advert-title-inner.qa-advert-title.b-advert-title-inner--div::text").get(),
                'price': product.css("div.qa-advert-price::text").get(),
            }
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            next_page_url  = "https://jiji.com.et" + next_page
            yield response.follow(url=next_page_url, 
                                  callback=self.parse,
                                  meta=dict(
                                    playwright=True,
                                    playwright_include_page=True,
                                    playwright_page_methods=[
                                        PageMethod("wait_for_timeout", 10),
                                        ],
                                    errback=self.errback,
                            ))
    
    async def errback(self, failure):
        page = failure.request.meta["playwright"]
        await page.close()
        self.logger.error('Page closed due to an error: %s', failure)