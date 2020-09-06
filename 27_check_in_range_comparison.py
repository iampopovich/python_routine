import sys
import time

print(sys.version)


def timeit(f):
    def wrap(*args):
        t1 = time.time()
        f(*args)
        print(time.time() - t1)
        return(time.time() - t1)
    return wrap


@timeit
def comp1(a, b, c):
    return a <= c <= b


@timeit
def comp2(a, b, c):
    return c in range(a, b)


tnew = comp1(1, 100000000, 50534)
told = comp2(1, 100000000, 50534)
print(told - tnew)


############OUTPUT#############
# 3.7.3 (default, Apr  3 2019, 05:39:12)
# [GCC 8.3.0]
# 7.152557373046875e-07
# 2.86102294921875e-06
# -1.1444091796875e-05
