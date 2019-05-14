import requests
from bs4 import BeautifulSoup
import re
import constant
import json

class Webscrapper:

	def __init__(self):
		pass

	def crawl(self):
		#print("crawling began...")
		params_g = {'GLtype':	'gainer', 'IndxGrp':	'AllMkt', 'IndxGrpval':	'AllMkt', 'orderby':	'all'}
		page_g = requests.get(url = constant.URL_GAINER, params = params_g,) 
		#print(page_g.status_code)
		page_g.raise_for_status()	
		#Note: next pages are stored as well
		with open("content_gainer.html", 'r+') as f:
			f.write(page_g.text)	

		params_l = {'GLtype':	'loser', 'IndxGrp':	'AllMkt', 'IndxGrpval':	'AllMkt', 'orderby':	'all'}
		page_l = requests.get(url = constant.URL_LOOSER, params = params_l,) 
		#print(page_l.status_code)
		page_l.raise_for_status()	
		with open("content_looser.html", 'r+') as f:
			f.write(page_l.text)	



	def parse(self, page):
		#print("parsing began...\n")
		with open("content_gainer.html", encoding="utf8") as f:
			contents = f.read()
		soup = BeautifulSoup(contents, "html.parser")
		gainer_data = json.loads(soup.text)	
		gainer_content = gainer_data['Table']  

		gainer_records = []
		top_gainers = []
		for record in gainer_content[0:10]:
			rec = {
			'security_code': record['scrip_cd'],
			'security_name': record['scripname'],
			'group': record['scrip_grp'],
			'last_traded_price': record['ltradert'],
			'change_val': record['change_val'],
			'change_perc': record['change_percent']
			}
			
			gainer_records.append(rec)
			top_gainers.append(rec['security_name'])

		print("top 10 gainers:")
		for i,v in enumerate(top_gainers): print(i+1, ".", v)


		with open("content_looser.html", encoding="utf8") as f:
			contents = f.read()
		soup = BeautifulSoup(contents, "html.parser")
		looser_data = json.loads(soup.text)		
		looser_content = looser_data['Table'] 

		looser_records = []
		top_loosers = []
		for record in looser_content[0:10]:
			rec = {
			'security_code': record['scrip_cd'],
			'security_name': record['scripname'],
			'group': record['scrip_grp'],
			'last_traded_price': record['ltradert'],
			'change_val': record['change_val'],
			'change_perc': record['change_percent']
			}
			
			looser_records.append(rec)
			top_loosers.append(rec['security_name'])
		
		print("\ntop 10 loosers:")
		for i,v in enumerate(top_loosers): print(i+1, ".", v)


def main():
	ws = Webscrapper()	
	page = ws.crawl()
	ws.parse(page = 'no need to pass page for now')

if __name__ == '__main__':
	main()

#create file, write it, parse it, then delete it.