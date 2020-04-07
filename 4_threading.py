import threading
import random
import time
import argparse

def init_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-b', metavar='BLOCK_SIZE', type = int)
	parser.add_argument('-t', metavar = 'THREAD_NUM', type = int, choices=(range(1,5)))
	return parser

def init_slicer(block,size):
	out = []
	chunk = block.__len__()//size
	for _ in size:
		out.append(block[:chunk])
		block = block[chunk:]
	return out

def timeit(func):
	def wrapper():
		t1 = time.now()
		func()
		t2 = time.now() - t1
		return t2
	return wrapper

def worker():

	return None

def main():
	parser = init_parser()
	args = parser.parse_args()
	block = [random.random() for i in range(args.b)]
	chunks = init_slicer(block, args.t)
	return None

if __name__ == '__main__':
	main()