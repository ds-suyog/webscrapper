import requests
from bs4 import BeautifulSoup
import re
#import constant
import json

class Webscrapper:

	def __init__(self):
		self._url = "https://www.bseindia.com/"

	def crawl(self):
		page = requests.get(self._url)  
		#constant.URL		
		print(page.headers['content-type'])
		print(page.encoding)
		print(page.status_code)  

		request_url = "https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=gainer&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all"
		params = {'GLtype':	'gainer', 'IndxGrp':	'AllMkt', 'IndxGrpval':	'AllMkt', 'orderby':	'all'}
		page = requests.get(url = request_url, params = params,) 
		print(page.status_code)
		page.raise_for_status()
		page_txt = page.text	

		with open("content.html", 'r+') as f:
			print(f.write(page_txt))	

		return page


	def parse(self, page):
		print("parsing...")

		with open("content.html", encoding="utf8") as f:
			contents = f.read()
		soup = BeautifulSoup(contents, "html.parser")
		
		#soup = BeautifulSoup(page.text, features="html.parser") #  <class 'bs4.BeautifulSoup'>, by default it uses features as best available html-parser
		
		data = json.loads(soup.text)
		print(type(data))		
		print(data.keys())




def main():
	ws = Webscrapper()	
	#page = ws.crawl()
	ws.parse(page = 'no need to pass for now')

if __name__ == '__main__':
	main()
