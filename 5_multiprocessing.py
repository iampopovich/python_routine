import multiprocessing
import math
import argparse
import time

def init_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument()
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
	return None

if __name__ == '__main__':
	main()