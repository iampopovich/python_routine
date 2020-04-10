import threading
import random
import time
import argparse
import math

def init_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-b', metavar='BLOCK_SIZE', type = int, required = True)
	parser.add_argument('-t', metavar = 'THREAD_NUM', type = int, choices=(range(1,5)), required=True)
	return parser

def init_slicer(block,size):
	out = []
	block = [0,1,2,3,4,5,6,7,8,9]
	chunk = block.__len__()//size
	for _ in range(0,size):
		if _ == size - 1: 
			out.append(block)
		else:
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

def worker(chunk):
	chunk = list(map(lambda x: x**2, chunk))
	print(chunk)
	return None

def main():
	parser = init_parser()
	args = parser.parse_args()
	block = [random.random() for i in range(args.b)]
	chunks = init_slicer(block, args.t)
	threads = []
	for ch in chunks:
		t = threading.Thread(target=worker, args=(ch,))
		threads.append(t)
		t.start()
	return None

if __name__ == '__main__':
	main()