# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from copy import deepcopy
import hashlib
from scrapy.utils.python import to_bytes


class MeizituspiderPipeline:
    def process_item(self, item, spider):
        return item


class MeizituImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("下载...", item['img_src'])
        yield scrapy.Request(item['img_src'], headers={"Referer": "https://www.mzitu.com/"}, meta={"item": deepcopy(item)})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return '%s/%s.jpg' % (item["title"], image_guid)
