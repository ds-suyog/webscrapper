import requests
from bs4 import BeautifulSoup
import re
import constant
import json

class Webscrapper:

	def __init__(self):
		pass

	def crawl(self):

		params_g = {'GLtype':	'gainer', 'IndxGrp':	'AllMkt', 'IndxGrpval':	'AllMkt', 'orderby':	'all'}
		page_g = requests.get(url = constant.URL_GAINER, params = params_g,) 
		print(page_g.status_code)
		page_g.raise_for_status()	
		#Note: next pages are stored as well, which 
		with open("content_gainer.html", 'r+') as f:
			print(f.write(page_g.text))	

		params_l = {'GLtype':	'loser', 'IndxGrp':	'AllMkt', 'IndxGrpval':	'AllMkt', 'orderby':	'all'}
		page_l = requests.get(url = constant.URL_LOOSER, params = params_l,) 
		print(page_l.status_code)
		page_l.raise_for_status()	
		with open("content_looser.html", 'r+') as f:
			print(f.write(page_l.text))	



	def parse(self, page):
		print("parsing...")

		with open("content_gainer.html", encoding="utf8") as f:
			contents = f.read()
		soup = BeautifulSoup(contents, "html.parser")

		gainer_data = json.loads(soup.text)		# data class dict
		gainer_content = gainer_data['Table']   #value class list
		#print(gainer_content[0])

		gainer_records = []
		top_gainers = []
		for record in gainer_content[0:10]:
			rec = {'security_code': record['scrip_cd'],
			'security_name': record['scripname'],
			'group': record['scrip_grp'],
			'last_traded_price': record['ltradert'],
			'change_val': record['change_val'],
			'change_perc': record['change_percent']}
			
			gainer_records.append(rec)
			top_gainers.append(rec['security_name'])

		for i,v in enumerate(top_gainers): print(i+1, ".", v)



def main():
	ws = Webscrapper()	
	#page = ws.crawl()
	ws.parse(page = 'no need to pass for now')

if __name__ == '__main__':
	main()
