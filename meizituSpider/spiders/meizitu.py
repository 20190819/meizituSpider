import scrapy
from ..items import MeizituspiderItem
from copy import deepcopy


class MeizituSpider(scrapy.Spider):
    name = 'mz'
    allowed_domains = ['www.mzitu.com', "tbweb.iimzt.com"]
    start_urls = ['https://www.mzitu.com/page/1/']

    def parse(self, response):
        li_list = response.xpath('//ul[@id="pins"]/li')
        for li in li_list:
            title = li.xpath('./span/a/text()').get()
            src = li.xpath('./span/a/@href').get()
            # 内页
            yield scrapy.Request(src, callback=self.parseDetail, meta={"title": deepcopy(title)})
        # 翻页
        next_page = response.xpath(
            "//div[@class='nav-links']/a[contains(@class,'next')]/@href").get()
        if(next_page):
            yield scrapy.Request(next_page, callback=self.parse)

    def parseDetail(self, response):
        item = MeizituspiderItem()
        item["title"] = response.meta["title"]
        print("标题...", item["title"])
        item["img_src"] = response.xpath("//p/a/img/@src").get()
        yield item
        next_page_text = response.xpath(
            "//div[@class='pagenavi']/a[last()]/span/text()").get()
        # 内页翻页
        if(next_page_text == "下一页»"):
            print("内页翻页", next_page_text)
            next_page = response.xpath(
                "//div[@class='pagenavi']/a[last()]/@href").get()
            yield scrapy.Request(next_page, callback=self.parseDetail, meta={"title": deepcopy(item["title"])})
