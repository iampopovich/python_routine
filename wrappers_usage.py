from time import time

def timeit(func):
	def wrapper(*args,**kwargs):
		t1 = time()
		func(*args,**kwargs)
		t2 = time() - t1
		print("%0.10f"%t2)
		return func(*args,**kwargs)
	return wrapper
	
@timeit
def fiboNumbers(num):
	fn = [0,1]
	for i in range(int(num) - len(fn)):
		fn.append(fn[i]+fn[i+1])
	return fn
	
def main():
	num = input("how many numbers do you want to get?  ")
	print(fiboNumbers(num))
	
if __name__ == "__main__":
	main()
	
