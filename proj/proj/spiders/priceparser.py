# -*- coding: utf-8 -*-
import scrapy
import time
from .config import urlMap 

class PriceParserSpider(scrapy.Spider):
    name = "priceparser"
    allowed_domains = ["arukereso.hu"]
    start_urls = urlMap.keys()
    with open("result.jl","a") as f: 
        f.write('{ "crawl-time" : ' + str(time.time()) + " }\n") #new crawl marker

    def parseOne(self,string):
        attribList = string.decode().split('onclick')[1].split('target')[0]
        attribs = attribList.split(',')
        return '{ "' + "-".join(attribs[-9].split("-")[:-1]).strip().strip("'") + '" : "' + attribs[-2].strip().strip("'") + '" }'

    def parse(self, response):
        prices = response.xpath('//a[@class="price"]')
        with open("result.jl","a") as f: 
            f.write('{ "name" : "' + urlMap[response.url] + '" }\n')
            res = prices.extract()
            for r in res: 
                f.write(self.parseOne(r.encode('utf-8')) + "\n") 
        diagram = response.xpath('//*[@id="offers"]/div[5]/div/script/text()')
        with open("diagram_data.jl","a") as f: 
            f.write('{ "name" : "' + urlMap[response.url] + '" }\n')
            r = diagram.extract_first()
            f.write(self.parseDiagramData(r) + "\n") 

    def parseDiagramData(self, data):
        result = ""
        data
        for r in data.split("[[")[1:3]: 
            result += "{}\n["
            i = iter(r.split(","))
            result += "\n".join(map(",".join,zip(i,i)))

            #for c in r.split(','):
            #    result += c + "\n"
        return result

