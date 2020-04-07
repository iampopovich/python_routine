import os 
import sys
import argparse
import re

def init_argparser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', metavar = 'PROCESS_NAME', type = 'str',
		help = 'укажи имя или часть имени процесса', required=True)
	parser = argparse.add_argument('-d', metavar = 'DESTROY', action = 'store_true')
	parser = argparse.add_argument('-s', metavar = 'SEARCH', action = 'store_true')
	return parser

def kill_process(name):
	return None

def search_process(name):
	return None

def main():
	parser = init_argparser()
	args = parser.parse_args()
	if args.d: kill_process(args.p)
	if args.s: search_process(args.p)