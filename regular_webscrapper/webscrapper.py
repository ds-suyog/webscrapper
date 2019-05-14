import requests
from bs4 import BeautifulSoup
import re

class Webscrapper:
	_url = "https://www.bseindia.com/"

	def __init__(self):
		pass

	def crawl(self):
		page = requests.get(Webscrapper._url)  #<class 'requests.models.Response'>
		print(page.headers['content-type'])
		print(page.encoding)
		print(page.status_code)  # 200 => success, 403 => forbidden, 404 => not found

		params = {'filter': ''} 
		#c = page.content   # <class 'bytes'>
		txt = page.text	# <class 'str'>

		# with open("content.txt", 'r+') as f:
		# 	print(f.write(txt))	
		return page

	def parse(self, page):
		soup = BeautifulSoup(page.text, features="html.parser") #  <class 'bs4.BeautifulSoup'>, by default it uses features as best available html-parser
		for link in soup.find_all('a'):
			print(link.get('href'))

		# with open("content.txt", 'r+') as f:
		# 	f.truncate()


def main():
	ws = Webscrapper()	
	page = ws.crawl()
	ws.parse(page)

if __name__ == '__main__':
	main()

		# with open("content.txt", 'r+') as f:
		# 	print(f.write(txt))	

