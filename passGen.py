#ver:0.1.0
import string
import random
import sys
import os
import argparse

def initArgParser():
	p = argparse.ArgumentParser(description = "Select some options: ")
	p.add_argument("-n", "--NUMBER", type = int, default = 10, required = True, help = "pick a length of password")
	p.add_argument("-r", "--ROW", type = int, default = 1, required = False, help = "pick a number to generate few passwords")
	p.add_argument("-s", "--SYMBOL", default = False, required = False, action = "store_true", help = "include uppercase/lowercase symbol in password chars")
	p.add_argument("-l", "--LWC", default = False, required = False, action = "store_true", help = "include lowercase symbol in password chars") 
	p.add_argument("-u", "--UPC", default = False, required = False, action = "store_true", help = "include uppercase symbol in password chars" ) 
	p.add_argument("-d", "--DGT", default = False, required = False, action = "store_true", help = "include digits in password chars") 
	# p.add_argument("-p", "--PUN", default = False, required = False, action = "store_true", help = "include punctuation in password chars") 
	# p.add_argument("-w", "--WSP", default = False, required = False, action = "store_true", help = "include whitespace in password chars") 
	return p

def genPassword(params):
	pwds = []
	charset = ""
	if params.SYMBOL:
		charset += string.ascii_letters
	else:
		if params.LWC : charset += string.ascii_lowercase 
		elif params.UPC : charset += string.ascii_uppercase
		else: charset += string.ascii_letters
	if params.DGT : charset+= string.digits
	# if params.PUN : charset+= string.punctuation
	# if params.WSP: charset+= string.whitespace
	for i in range(params.ROW):
		pwd = "".join(random.choice(charset) for i in range(params.NUMBER))
		pwds.append(pwd)
	print("\n".join(pwds))
	return None

def main():
	parser = initArgParser()
	args = parser.parse_args()
	genPassword(args)
	return None

if __name__ == "__main__":
	main()
