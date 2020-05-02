from iterrools import permutation
from bs4 import *
from argparse import *
import requests
from urllib.parse import urlparse
import json
import os
import sys
import re
import time
import threading
import user_agent


def scrapper(engine, queries, outFile):
	fileOutPath = outFile
	for i,query in enumerate(queries):
		time.sleep(30)
		uagent = user_agent.generate_user_agent()
		results = []
		response = search(query, tld="co.in", num=80, start = 0, stop=79, pause=70, user_agent = uagent)
		for pos,resp in enumerate(response):
			# target = re.search(r"baehr.ru|baehrrussia|behrru|podologclub|nautilus2000|uchebnyj_tsentr_nautilus|pedicurenautilus|pedicure_nautilus|www.krasota.spb.ru",resp)
			if target is None: continue
			else:
				result = "{0};{1};{2};{3}" %(engine,query.strip("\n"), pos, resp)
				results.append(result)
		with open(fileOutPath,"a") as output:
			output.write("%s\n"%("\n".join(results)))
		glob_index_google+=1

# def permuteResult(func):
	
# 	def permuteWrapper():
# 		generatedSet = func(args)
# 	return permuteResult

def generateRequests(args): 
	result = []
	if "-kw" in args:
		keywords = None
	if "-fkw" in args:
		with open("keywordFile","r") as fkw:
			keywords = fkw.readlines().split()
	return keywords.permutation(4)

def generateTargets(args)
	targets = []
	if "-tg" in args:
		targets = None
	if "-tgf" in args:
		with open("tgf", "r") as tgf:
			targets = tgf.readlines().split()
	return targets

def generateSearches(args):
	searches = []
	if "-sg" in args:
		searches = None
	if "-sgf" in args:
		with open("sgf", "r") as sgf:
			searches = sgf.readlines().split()
	return searches

def main(args):
	queries = generateQueries(args)
	targets = generateTergets(args)
	searchEngines = generateSearches(args)
	outFile = None # if flag -o generate output csv
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
			# print(exr)
			# print("waiting for a minute...")
			# time.sleep(45)
			continue
	print("done scrapping at {}...".format(time.time()))
	pass

if __name__ == "__main__":
	main(sys.argv)
