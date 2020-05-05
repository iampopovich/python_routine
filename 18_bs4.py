from iterrools import permutation
from bs4 import *
import argparse
import requests
from urllib.parse import urlparse
import json
import os
import sys
import re
import time
import threading
import user_agent
#kw - keywords in arguments
#fkw - keywords file

class Scrapper:

	def __init__(self):
		self.path_file_out = None
		self.search_engine = None
		self.user_agent = user_agent.generate_user_agent()
		self.url_target = None
		self.keywords = None
		self.level = 2

	def set_user_agent(self):
		self.user_agent = user_agent.generate_user_agent()

	def get_headers(self, lang = ''):
		headers_Get = {
			'User-Agent': self.user_agent,
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'DNT': '1',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1'
		}
		return headers_Get

	def set_url_target(self,url):
		# target = re.search(r"baehr.ru|baehrrussia|behrru|podologclub|nautilus2000|uchebnyj_tsentr_nautilus|pedicurenautilus|pedicure_nautilus|www.krasota.spb.ru",resp)
		self.url_target = url

	def set_level(self,level):
		self.level = level

	def set_engine(self, engine):
		if engine == 'google': self.engine = 'https://www.google.com/search?q='
		if engine == 'yandex': self.engine = 'https://yandex.ru/search/?text='
		if engine == 'duckduck': self.engine = 'https://duckduckgo.com/?q='

	def scrap_queries(self, queries):
		s = requests.Session()
		for i,q in enumerate(queries):
			query = '+'.join(q)
			results = []
			response = requests.get(self.engine + query, headers = self.get_headers())
			soup = BeautifulSoup(r.text, "html.parser")
			# output = []
			# for searchWrapper in soup.find_all('h3', {'class':'r'}): #this line may change in future based on google's web page structure
			# 	url = searchWrapper.find('a')["href"] 
			# 	text = searchWrapper.find('a').text.strip()
			# 	result = {'text': text, 'url': url}
			# 	output.append(result)


			for position,resp in enumerate(response):
				if target is None: continue
				else:
					result = "{0};{1};{2};{3}" %(engine,query.strip("\n"), position, resp)
					results.append(result)
			with open(self.path_file_out,'a') as output:
				output.write("%s\n"%("\n".join(results)))
			time.sleep(30)

	def set_keywords(self, keywords):
		result = []
		for _ in range(n):
			result.extends(itertools.permutations(keywords,self.level)) 
		self.keywords = result

	def set_keywords_from_file(self, file):
		result = []
		with open(file, 'r') as f:
			json_load = json.load(f)
			keywords = json_load['keywords']
		for _ in range(n):
			result.extends(itertools.permutations(keywords,self.level)) 
		self.keywords = result

	def get_config():
		return None #parsed json

def init_argparser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-kwf', 
		metavar = 'KEYWORDS_FILE', 
		action = 'store_true', 
		help = 'укажи имя или часть имени процесса')
	parser.add_argument('-kw', 
		help = '', 
		type = str)
	parser.add_argument('-se',
		help = 'choose search engine', 
		type = str, 
		choices = ['google','yandex','duckduck'])
	parser.add_argument('-pl', 
		metavar = 'PERMUTATION_LEVEL',
		type = int,  
		help = 'how many permutations you want to check', 
		action = 'store_true')
	parser.add_argument('-tg',
		metavar = 'TARGET_MASK',
		type = str,
		help = 'type mask of target source you want to find',
		required = True)
	return parser

def main():
	parser = init_argparser()
	args = parser.parse_arguments()
	scrapper = Scrapper()
	if args['pl']: scrapper.set_level(args['pl'])
	if args['tg']: pass
	if args['se']: scrapper.set_engine(args['se'])
	scrapper.generate_requests(keywords)

	while True:
		try:
			if glob_index_google == len(queries): break
			qu = queries[glob_index_google:]
			tr1 = threading.Thread(target = scrapper, args = (qu))
			tr1.start()
			print("new thread start at {}...".format(time.time()))
			tr1.join()
			print("thread killed at {}...".format(time.time()))
			time.sleep(15)
		except Exception as ex:
			continue
	print("done scrapping at {}...".format(time.time()))
	pass

if __name__ == "__main__":
	main()
