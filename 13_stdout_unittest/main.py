import os
import sys
import subprocess
import threading
import unittest
import logging
import random
import time
import parser

#main должен стартовать один процесс для генерации лога, второй процесс с парсером 
#метод второго процесса должен принимать пид генерирующего процесса  

def main():
	file = 'output.log'
	threads = []
	t_writer = threading.Thread(target = writer, args=(file,),daemon = True)
	t_parser = threading.Thread(target = parser_file, args=(file,'3',), daemon=True)
	threads.extend([t_writer,t_parser])
	for t in threads: t.start()
	for t in threads: t.join()

		
if __name__ == '__main__':
	main()