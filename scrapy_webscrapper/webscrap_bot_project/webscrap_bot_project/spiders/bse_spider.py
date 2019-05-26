import scrapy
from scrapy.crawler import CrawlerProcess

class BseSpider(scrapy.Spider): 
    name = "extract"                 
    def start_requests(self): 
        urls = ['https://www.bseindia.com/', ]        
        for url in urls: 
            yield scrapy.Request(url = url, callback = self.parse) 

        def parse(self, response):
        	title = response.css('title::text').extract_first()
        	links = response.css('a::attr(href)').extract()

        	for link in links:
        		yield
        		{
        		'title': title,
        		'links': link
        		} 