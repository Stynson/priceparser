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
        attribList = string.decode("utf-8").split('onclick')[1].split('target')[0]
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
        with open("chart_data.jl","a") as f: 
            f.write('{ "name" : "' + urlMap[response.url] + '" }\n')
            r = diagram.extract_first()
            f.write(self.parseDiagramData(r) + "\n") 

    def parseDiagramData(self, data):
        if data:
            headers = ["minimum","average"]
            result = "" 
            hack = 0
            for r in data.split("[[")[1:3]: 
                result += '{ "header" : "' + headers[hack] + '" }\n{'
                hack += 1
                i = iter(r.split(","))
                zipped = "\n".join(map(",".join,zip(i,i)))
                zipped = zipped.replace("]]","]")
                zipped = zipped.replace("]","}")
                zipped = zipped.replace("[","{")
                zipped = zipped.replace(", ",":")
                result += zipped + "\n" 
            return result
        else: return ""

