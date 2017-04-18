# -*- coding: utf-8 -*-
import scrapy


class PriceParserSpider(scrapy.Spider):
    name = "priceparser"
    #allowed_domains = ["example.com"]
    start_urls = ['https://www.arukereso.hu/szamitogep-haz-c3085/zalman/m1-p230370475/']

    def parseOne(self,string):
        attribList = string.split('onclick')[1]
        attribs = attribList.split(',')
        return '{ "' + "-".join(attribs[-9].split("-")[:-1]).strip().strip("'") + '" : "' + attribs[-2].strip().strip("'") + '" }'

    def parse(self, response):
        #xpath = response.xpath('//*[@id="offer-list"]/div[1]/div[1]/div/div[5]/a')
        xpath = response.xpath('//a[@class="price"]')
        with open("result.jl","w") as f: 
            res = xpath.extract()
            for r in res: 
                f.write(self.parseOne(r) + "\n")




#from scrapy import signals
#from scrapy.exporters import XmlItemExporter

#class XmlExportPipeline(object):

     #def __init__(self):
        #self.files = {}

     #@classmethod
     #def from_crawler(cls, crawler):
         #pipeline = cls()
         #crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         #crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         #return pipeline

    #def spider_opened(self, spider):
        #file = open('%s_products.xml' % spider.name, 'w+b')
        #self.files[spider] = file
        #self.exporter = XmlItemExporter(file)
        #self.exporter.start_exporting()

    #def spider_closed(self, spider):
        #self.exporter.finish_exporting()
        #file = self.files.pop(spider)
        #file.close()

    #def process_item(self, item, spider):
        #self.exporter.export_item(item)
        #return item

