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
	def wrapper(*args, **kw):
		t1 = time.time()
		func(*args, **kw)
		t2 = time.time() - t1
		print(t2)
	return wrapper

@timeit
def worker(chunk):
	chunk = list(map(lambda x: x**2, chunk))
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

#python3 4_threading.py  -b 9000000
#1 : 
	#7.05718994140625e-05
#2 : 
	#5.7220458984375e-05
	#2.1457672119140625e-05
#3 : 
	# 3.314018249511719e-05
	# 2.5033950805664062e-05
	# 1.5020370483398438e-05
#4 :
	# 3.147125244140625e-05
	# 2.5033950805664062e-05
	# 2.8133392333984375e-05
	# 2.765655517578125e-05