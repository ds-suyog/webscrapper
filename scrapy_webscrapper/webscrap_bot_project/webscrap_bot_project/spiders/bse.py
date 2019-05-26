import scrapy
from scrapy.crawler import CrawlerProcess

class BseSpider(scrapy.Spider):
	name = "bse"
	print("==============")
	def start_requests(self):
		url = 'https://www.bseindia.com/'
		yield scrapy.Request(url = url, callback = self.parse)

	def parse(self, response):
		print("========     =============       ===========")

