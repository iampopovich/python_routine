import sys
import time
from string import Template

print(sys.version)


def timeit(f):
    def wrap(*args):
        t1 = time.time()
        f(*args)
        print("%s return time : %s" % (f.__name__, time.time() - t1))
        return(time.time() - t1)
    return wrap


@timeit
def format1(p1, p2, p3):
    return "%s %s %s" % (p1, p2, p3)


@timeit
def format2(p1, p2, p3):
    return "{0} {1} {2}".format(p1, p2, p3)


@timeit
def format3(p1, p2, p3):
    return f'{p1} {p2} {p3}'


@timeit
def format4(p1, p2, p3):
    t = Template('$p1 $p2 $p3')
    t.substitute(p1=p1, p2=p2, p3=p3)


@timeit
def format5(p1, p2, p3):
    return " ".join([p1, p2, p3])


@timeit
def format6(p1, p2, p3):
    return p1 + p2 + p3


format1("abcde", "fghi", "jklmnopqrstuv")
format2("abcde", "fghi", "jklmnopqrstuv")
format3("abcde", "fghi", "jklmnopqrstuv")
format4("abcde", "fghi", "jklmnopqrstuv")
format5("abcde", "fghi", "jklmnopqrstuv")
format6("abcde", "fghi", "jklmnopqrstuv")


"""
3.7.3 (default, Apr  3 2019, 05:39:12) 
[GCC 8.3.0]
format1 return time : 1.6689300537109375e-06
format2 return time : 2.1457672119140625e-06
format3 return time : 1.1920928955078125e-06
format4 return time : 1.5020370483398438e-05
format5 return time : 9.5367431640625e-07
format6 return time : 7.152557373046875e-07
"""
