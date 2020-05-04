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

	def set_set_url_target(self,url):
		# target = re.search(r"baehr.ru|baehrrussia|behrru|podologclub|nautilus2000|uchebnyj_tsentr_nautilus|pedicurenautilus|pedicure_nautilus|www.krasota.spb.ru",resp)
		self.url_target = url

	def init_scrapper(self, engine, queries):
		for i,query in enumerate(queries):
			time.sleep(30)
			results = []
			response = search(query, tld="co.in", num=80, start = 0, stop=79, pause=70, user_agent = uagent)
			for position,resp in enumerate(response):
				if target is None: continue
				else:
					result = "{0};{1};{2};{3}" %(engine,query.strip("\n"), position, resp)
					results.append(result)
			with open(self.path_file_out,'a') as output:
				output.write("%s\n"%("\n".join(results)))
			glob_index_google+=1

	def generate_requests(args): 
		result = []
		if "-kw" in args:
			keywords = None
		if "-fkw" in args:
			with open("keywordFile","r") as fkw:
				keywords = fkw.readlines().split()
		return keywords.permutation(4)

	def get_config():
		return None #parsed json

def init_argparser():
	return None

def main():
	argparser = init_argparser()
	scraper = Scrapper()

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
