from multiprocessing import Process, cpu_count
import argparse
from time import time
from random import random


def init_parser():
    cores = cpu_count()
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', metavar='BLOCK_SIZE', type=int, required=True)
    parser.add_argument('-p', metavar='PROC_NUM', type=int,
                        choices=(range(1, cores+1)), required=True)
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
    def wrapper(*args, **kwargs):
        t1 = time()
        func(*args, **kwargs)
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
    chunks = init_slicer(block, args.p)
    procs = list()
    for ch in chunks:
        p = Process(target=worker, args=(ch,))
        procs.append(p)
        p.start()
    for p in procs:
        p.join()
    return None


if __name__ == '__main__':
    main()

# python3 5_multiprocessing.py -b 9000000
# 1 :
    # 5.860256671905518
# 2 :
    # 3.0215048789978027
    # 3.0367324352264404
# 3 :
    # 1.7808728218078613
    # 1.8975632190704346
    # 2.217034101486206
# 4 :
    # 2.32314395904541
    # 2.3880319595336914
    # 2.738544464111328
    # 3.0047199726104736
