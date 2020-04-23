import os
import sys
import subprocess
import threading
import unittest
import logging
import random
import time


# имеет смысл описать парсер классом


def writer(file):
	while True:
		with open(file,'a') as f:
			f.write('{}\n'.format(random.randint(0,10)))
		time.sleep(1)

def parser_proc(proc, match = '100'):
	while True:
		line = proc.stdout.readline()
		if line:
			if match in line:
				print('{} FOUND!'.format(match))
		if line.__len__() == 0 and proc.poll() is not None:
			break 
	rc = proc.poll()
	return rc

def parser_file(file,match = '100'):
	while True:
		try:
			with open(file,'r') as f:
				if match in f.readlines()[-1:]:
					print('{} was found!'.format(match))#мб вот здесь лок аута
					# sys.exit()
		except Exception as ex:
			logging.error('{}'.format(ex))
			continue

def main():
	file = 'output.log'
	threads = []
	# proc = subprocess.Popen(['/bin/sh','-c','{}/generator.sh'.format(os.getcwd())],stdout=subprocess.PIPE, shell = True, encoding = 'utf-8')
	t_writer = threading.Thread(target = writer, args=(file,),daemon = True)
	t_parser = threading.Thread(target = parser_file, args=(file,'3',), daemon=True)
	threads.extend([t_writer,t_parser])
	for t in threads: t.start()
	for t in threads: t.join()

		
if __name__ == '__main__':
	main()