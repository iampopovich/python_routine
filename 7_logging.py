import threading
import logging
import argparse
import random

def init_argparser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-b', metavar='BLOCK_SIZE', type = int, required = True)
	parser.add_argument('-t', metavar = 'THREAD_NUM', type = int, choices=(range(1,5)), required=True)
	return parser

def init_slicer(block, size):
	out = []
	chunk = block.__len__()//size
	for _ in range (0, size):
		if _ == size - 1: out.append(block)
		else:
			out.append(block[:chunk])
			block = block[chunk:]
	return out

def worker(data):
	data = list(map(lambda x: x+1 , data))
	print(data)
	return data

def main():
	parser = init_argparser()
	args = parser.parse_args()
	threads = []
	block = [random.random() for i in range(0, args.b)]
	chunks = init_slicer(block, args.t)
	for ch in chunks:
		t = threading.Thread(target=worker, args=(ch,))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	return None

if __name__ == '__main__':
	main()