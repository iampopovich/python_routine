import sys
import string
import random

def genName( size = 30, chars = string.ascii_letters + string.digits):
	return "".join(random.choice(chars) for i in range(size)) 

def genNumber( size = 15, chars = string.ascii_digits):
	return "".join(random.choise(chars) for i in range(size))

def genEmail(size = 10 , chars = string.ascii_letters + string.digits):
	name = "".join(random.choice(chars) for i in range(size)) 
	domain = "".join(random.choice(chars) for i in range(size))
	region = "".join(random.choice(string.ascii_letters) for i in range(3))
	return "{0}@{1}.{2}".format(name, domain,region)
	
def genCardNum():
	pass

def genPoints():
	pass

def genBirthDate():
	pass

def main(args):
	with open ("deg.csv", "a") as out:
		try:
			for i in range (args[1]):
				name = genName()
				number = genNumber()
				email = genEmail()
				points = genPoints()
				bday = genBirthDate()
			out.write(";".join([name,number,email,points,bday]))
		except: return "oops"

if __name__ == "__main__":
	main(sys.argv)
