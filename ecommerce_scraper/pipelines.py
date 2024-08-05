# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import logging
import hashlib

class customImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        image_perspective = item["name"].lower().replace(" ", "_")
        image_filename = f"ecommerce_project/data/images{image_perspective}.jpg"

        return image_filename

class EcommerceScraperPipeline:
    def process_item(self, item, spider):
        return item
