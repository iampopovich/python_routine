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
def comp1(a,b,c):
	return a<=c<=b
 
@timeit
def comp2(a,b,c):
	return c in range(a,b)
 
tnew = comp1(1,100000000,50534)
told = comp2(1,100000000,50534)
print(told - tnew)
