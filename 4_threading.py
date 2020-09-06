from threading import Thread
from random import random
from time import time
import argparse


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', metavar='BLOCK_SIZE', type=int, required=True)
    parser.add_argument('-t', metavar='THREAD_NUM', type=int,
                        choices=(range(1, 5)), required=True)
    return parser


def init_slicer(block, size):
    out = []
    chunk = block.__len__()//size
    for _ in range(0, size):
        if _ == size - 1:
            out.append(block)
        else:
            out.append(block[:chunk])
            block = block[chunk:]
    return out


def timeit(func):
    def wrapper(*args, **kw):
        t1 = time()
        func(*args, **kw)
        t2 = time() - t1
        print(t2)
    return wrapper


@timeit
def worker(chunk):
    chunk = list(map(lambda x: x**2, chunk))
    return None


def main():
    parser = init_parser()
    args = parser.parse_args()
    block = [random() for i in range(args.b)]
    chunks = init_slicer(block, args.t)
    threads = []
    for ch in chunks:
        t = Thread(target=worker, args=(ch,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return None


if __name__ == '__main__':
    main()
