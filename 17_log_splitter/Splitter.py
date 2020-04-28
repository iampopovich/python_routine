import re
import os
import sys
import argparse 
import threading

class Splitter():
	def __init__(self):
		self.application = None
		self.level = None
		self.path_original_log = None

	def set_level(self, level = None):
		if level:
			self.level = level
		else:
			self.level = input('type log level: ')

	def set_app(self, app = None):
		if app:
			self.app = app
		else:
			self.app = input('type app name: ')

	def set_log_file(self, file = None):
		if file:
			self.path_original_log = file
		else:
			self.path_original_log = input('drop original log file into terminal: ')

	def split_file(self, apps = None, levels = None):

		return None

def main():
	# parser
	split = Splitter()
	split.set_level() #pass level argument
	split.set_app()
	split.set_log_file()
	split.split_file()

if __name__ == '__main__':
	main()
