from itertools import permutation
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

ENGINES = {
	'google': 'https://www.google.com/search?q='
	'yandex': 'https://yandex.ru/search/?text='
	'duckduck': 'https://duckduckgo.com/?q='
	}

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
		# target = re.search(r'baehr.ru|baehrrussia|behrru|podologclub|nautilus2000|uchebnyj_tsentr_nautilus|pedicurenautilus|pedicure_nautilus|www.krasota.spb.ru',resp)
		self.url_target = url

	def set_level(self,level):
		self.level = level

	def set_engine(self, engine):
		self.engine = ENGINES[engine]

	def scrap_responses(self, queries):
		s = requests.Session()
		for q in queries:
			query = '+'.join(q)
			results = {}
			r = requests.get(self.engine + query, headers = self.get_headers())
			soup = BeautifulSoup(r.text, 'html.parser')
			topics = soup.findAll('div',{'class':'g'})
			for index, t in enumerate(topics):
				topic_title = t.find('h3').getText()
				#if regexp is exist
				topic_url = t.find('div',{'class':'rc'}).find('a')['href']
				topic_index = index
				results[topic_url] = {
									'query': query,
									'title': topic_title,
									'engine': engine,
									'position': topic_index
									}
			with open(self.path_file_out,'a') as output:
				json.dump(results, output)
			time.sleep(30)

	def set_keywords(self, keywords):
		result = []
		for _ in range(self.level):
			result.extends(permutations(keywords,_)) 
		self.keywords = result

	def set_keywords_from_file(self, file):
		result = []
		with open(file, 'r') as f:
			json_load = json.load(f)
			keywords = json_load['keywords']
		for _ in range(self.level):
			result.extends(permutations(keywords,_)) 
		self.keywords = result

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
			print('new thread start at {}...'.format(time.time()))
			tr1.join()
			print('thread killed at {}...'.format(time.time()))
			time.sleep(15)
		except Exception as ex:
			continue
	print('done scrapping at {}...'.format(time.time()))
	pass

if __name__ == '__main__':
	main()
