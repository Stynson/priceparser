# -*- coding: utf-8 -*-
import scrapy
import time
from config import urlMap 

class PriceParserSpider(scrapy.Spider):
    name = "priceparser"
    allowed_domains = ["arukereso.hu"]
    start_urls = urlMap.keys()
    with open("result.jl","a") as f: 
        f.write('{ "crawl-time" : ' + str(time.time()) + " }\n") #new crawl marker

    def parseOne(self,string):
        attribList = string.split('onclick')[1].split('target')[0]
        attribs = attribList.split(',')
        return '{ "' + "-".join(attribs[-9].split("-")[:-1]).strip().strip("'") + '" : "' + attribs[-2].strip().strip("'") + '" }'

    def parse(self, response):
        xpath = response.xpath('//a[@class="price"]')
        with open("result.jl","a") as f: 
            f.write('{ "name" : "' + urlMap[response.url] + '" }\n')
            res = xpath.extract()
            for r in res: 
                f.write(self.parseOne(r.encode('utf-8')) + "\n") 
