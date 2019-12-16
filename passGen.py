#ver:0.0.2
import string
import random
import sys
import os
import argparse

def genPasswordList():
	pass

def initArgParser():
	p = argparse.ArgumentParser(description = "Select some options: ")
	p.add_argument("-f", metavar = "FILE", help = "generate password file in current directory")
	p.add_argument("-n", metavar = "NUMBER", help = "pick length of password")
	p.add_argument("-s", metavar = "SYMBOL", help = "include uppercase/lowercase symbol in password chars")
	p.add_argument("-l", metavar = "LWC", type = bool, default = False, help = "include lowercase symbol in password chars") 
	p.add_argument("-u", metavar = "UPC", type = bool, default = False, help = "include uppercase symbol in password chars" ) 
	p.add_argument("-N", metavar = "NUM", type = bool, default = False, help = "include numbers in password chars") 
	p.add_argument("-p", metavar = "PUN", type = bool, default = False, help = "include punctuation in password chars") 
	p.add_argument("-w", metavar = "WSP", type = bool, default = False, help = "include whitespace in password chars") 
	return p

def genPassword(params):
	pass

def main():
	parser = initArgParser()
	args = parser.parse_args()

if __name__ == "__main__":
	main()
