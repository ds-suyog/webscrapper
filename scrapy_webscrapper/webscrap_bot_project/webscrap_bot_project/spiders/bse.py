import scrapy
from scrapy.crawler import CrawlerProcess

class GainersSpider(scrapy.Spider):
	name = "bse_gainers"
	def start_requests(self):
		url = "https://www.bseindia.com/"
		yield scrapy.Request(url = url, callback = self.parse)

	def parse(self, response):
		print("======   ========== bse_gainers: parse!!")

class LoosersSpider(scrapy.Spider):
	name = "bse_loosers"
	def start_requests(self):
		urls = "https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=gainer&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all"
		yield scrapy.Request(url = url, callback = self.parse)

	def parse(self, response):
		print("======   ========== bse_loosers: parse!!")

class TrendingSpider(scrapy.Spider):
	name = "bse_trending"
	def start_requests(self):
		url = "https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=loser&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all"
		yield scrapy.Request(url = url, callback = self.parse)

	def parse(self, response):
		print("======   ========== bse_trending: parse!!")

