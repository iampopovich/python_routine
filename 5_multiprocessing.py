import multiprocessing
import math
import argparse
import time
import random

def init_parser():
	cores = multiprocessing.cpu_count()
	parser = argparse.ArgumentParser()
	parser.add_argument('-b', metavar='BLOCK_SIZE', type = int, required = True)
	parser.add_argument('-p', metavar = 'PROC_NUM', type = int, choices=(range(1,cores+1)), required=True)
	return parser

def timeit(func):
	def wrapper(*args,**kwargs):
		t1 = time.time()
		func()
		t2 = t1 - time.time()
		primt(t2)
	return wrapper

@timeit
def worker():
	return None

def main():
	parser = init_parser()
	args = parser.parse_args()
	block = [random.random() for i in range(args.b)]
	chunks = init_slicer(block, args.p)
	procs = list()
	# for ch in chunks:
		# p = multiprocessing.Process()
		# procs.append(p)
		# p._Popen()
	return None

if __name__ == '__main__':
	main()