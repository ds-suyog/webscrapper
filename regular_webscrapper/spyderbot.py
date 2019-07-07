import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import logging 
import json
import git 
from pymongo import MongoClient
import os
import git, sys; sys.path.append("{}/regular_webscrapper".format(git.Repo('.', search_parent_directories=True).working_tree_dir))
import constant
import time
from elasticsearch import helpers, Elasticsearch

class SpyderBot:

	def __init__(self):
		pass				

	def crawl(self):
    """Launch crawl process
    The instance method performs data acquisition.
    :param None
    :return None.
    """
		logger = self.getlogger('crawl')			
		logger.debug("\n\n================================= crawling started")	
		logger.info("selemium emulating firefox browser")

		driver = webdriver.Firefox(executable_path=r"{}".format(constant.GECKODRIVER_BIN), log_path='{}'.format(constant.LOGPATH['geckodriver']))
		page = driver.get(constant.BASE_URL)
		link = driver.find_element_by_link_text('Trending')
		link.click()
		driver.implicitly_wait(10)
		html_source = driver.page_source
		with open ("tmp/base_page_after_click.html", 'w') as f:	
			f.write(html_source)
		driver.close()

		params_g = {'GLtype':	'gainer', 'IndxGrp':	'AllMkt', 'IndxGrpval':	'AllMkt', 'orderby':	'all'}
		page_g = requests.get(url = constant.URL_GAINER, params = params_g,) 
		page_g.raise_for_status()	
		with open("tmp/content_gainer.html", 'w') as f:
			f.write(page_g.text)	

		params_l = {'GLtype':	'loser', 'IndxGrp':	'AllMkt', 'IndxGrpval':	'AllMkt', 'orderby':	'all'}
		page_l = requests.get(url = constant.URL_LOOSER, params = params_l,) 
		page_l.raise_for_status()	
		with open("tmp/content_looser.html", 'w') as f:
			f.write(page_l.text)	
		logger.info("crawling completed!")


	def parse(self): 
		logger = self.getlogger('parse')		
		logger.debug("\n\n=================================	parsing started")	

		logger.debug("parsing trending")
		with open ("tmp/base_page_after_click.html", 'r', encoding="utf8") as f:	
			contents = f.read()
		soup = BeautifulSoup(contents, "html.parser")
		div_u2d1 = soup.find_all('div', id = 'u2_d1')	
		trending = [ {'_id': self.crypt(anc.text), 'name': anc.text} for rank, anc in enumerate(div_u2d1[0].find_all('a'))]
		self.insert_one(trending, 'trending')
		self.bulk_insert(trending, 'bse_trending', 'trending')		
		os.remove("tmp/base_page_after_click.html")

		logger.debug("parsing gainers")
		with open("tmp/content_gainer.html", encoding="utf8") as f:
			contents = f.read()
		soup = BeautifulSoup(contents, "html.parser")
		gainer_data = json.loads(soup.text)	
		gainer_content = gainer_data['Table']  
		gainers = []
		top_gainer_names = []
		for i,doc in enumerate(gainer_content[0:10]):
			document = {
			'rank': i+1,
			'security_code': doc['scrip_cd'],
			'security_name': doc['scripname'],
			'group': doc['scrip_grp'],
			'last_traded_price': doc['ltradert'],
			'change_val': doc['change_val'],
			'change_perc': doc['change_percent']
			}
			gainers.append(document)
			top_gainer_names.append(document['security_name'])
		lst_g = ["%s.%s"%(i+1,v) for i,v in enumerate(top_gainer_names)]
		self.insert_one(gainers, 'gainers')
		self.bulk_insert(gainers, 'bse_gainers', 'gainers')
		os.remove('tmp/content_gainer.html')

		logger.debug("parsing loosers")
		with open("tmp/content_looser.html", encoding="utf8") as f:
			contents = f.read()
		soup = BeautifulSoup(contents, "html.parser")
		looser_data = json.loads(soup.text)		
		looser_content = looser_data['Table'] 
		loosers = []
		top_looser_names = []
		keys = ['security_code', 'security_name', 'group', 'last_traded_price', 'change_val', 'change_percent']
		for doc in looser_content[0:10]:
			values = [doc['scrip_cd'], doc['scripname'], doc['scrip_grp'], doc['ltradert'], doc['change_val'], doc['change_percent']]
			loosers.append(dict(zip(keys,values)))
		lst_l = ["%s.%s"%(i+1,v['security_name']) for i,v in enumerate(loosers)]		
		self.insert_one(loosers, 'loosers')
		self.bulk_insert(loosers, 'bse_loosers', 'loosers')
		os.remove("tmp/content_looser.html")
		logger.info("parsing completed!!")


	def getlogger(self, task, resume = 'False'):
		logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
		logger = logging.getLogger()
		fileh = logging.FileHandler(constant.LOGPATH[task], 'w') if resume == 'False' else logging.FileHandler(constant.LOGPATH[task], 'a')
		for hdlr in logger.handlers[:]:
  		    logger.removeHandler(hdlr)		
		logger.handlers = [fileh]
		return logger

	def crypt(self, to_encrypt):                                                            
		chars = [c for c in to_encrypt]
		keyy = []
		for c in chars:
			keyy.append(str(ord(c)))
		return ''.join(keyy)

	def getmongoclient(self, colname):
		try:
			myclient = MongoClient(constant.MONGODB_HOST, constant.MONGODB_PORT) 
		except:
			pass
		mydb = myclient[constant.BSE_DB]
		mycol = mydb[colname]
		return myclient, mydb, mycol

	def insert_one(self, data, colname):
		myclient, mydb, mycol = self.getmongoclient(colname)
		if colname in mydb.list_collection_names(): mydb[colname].remove()
		for doc in data:
			try:
				result = mydb[colname].insert_one(doc)							
			except Exception as e:
				pass									

	def insert_many(self, data, colname):
		myclient, mydb, mycol = self.getmongoclient(colname)
		if colname in mydb.list_collection_names(): mydb[colname].remove()
		mycol.insert(data)

	def mongodumpjson(self, colname, filepath):
		myclient, mydb, mycol = self.getmongoclient(colname)		
		cursor = mycol.find()
		with open (filepath, 'w', encoding="utf8") as f:
			docs = [doc for doc in cursor]
			json.dump(docs,f)

	def mongoimportjson(self, colname, filepath):		
		myclient, mydb, mycol = self.getmongoclient(colname)	
		with open(filepath, 'r', encoding="utf8") as f:
			docs = json.load(f)
			for doc in docs:
				try:
					result = mycol.insert_one(doc)
				except Exception as e:
					pass		

	def mongoimportbson(self, colname, filepath):
		myCmd = 'bsondump {} > {}'.format(filepath, filepath.replace('bson','json'))
		os.system(myCmd)
		os.system('ls {}}/tmp/bse'.format(constant.BASEDIR))
		self.mongoimportjson(colname, filepath.replace('bson','json'))

	def bulk_insert(self, data, indexname, doctype):
		from elasticsearch import helpers, Elasticsearch
		es = Elasticsearch()
		temp = {'_index': indexname,'_type': doctype}
		trending_bulk = list()
		for doc in data:
			del doc['_id']
			doc.update(temp)
			trending_bulk.append(doc)	
		helpers.bulk(es, trending_bulk, chunk_size=1000, request_timeout=200)

def main():
	ws = SpyderBot()	
	ws.crawl()
	ws.parse()

if __name__ == '__main__':
	main()


