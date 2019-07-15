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
	
