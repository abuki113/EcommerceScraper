import scrapy


class EcommerceSpiderSpider(scrapy.Spider):
    name = "ecommerce_spider"
    
    start_urls = ["https://www.carsdirect.com/new_cars/results"]

    def parse(self, response):
        pass
