'''
не решена проблема разделения слов , если пропущен пробел
не решена проблема с детектированием операционной системы
'''
import sys
import os
import shutil
import datetime as dt
import time as tt
import math
import argparse
#import langodetect
# import pyzbar
# import pyqrcoder #прочекай в записях еще 2е либы под qr из окб

LATIN_SYMBOLS = ["abcdefghijklmnopqrstuvwxyz"]
KYRILLIC_SYMBOLS = ["абвгдеёжзийклмнопрстуфхцчшщъыьэюя"]

def decode(path):
	decodedString = None
	return decodedString

def code(stringInput, terminal = False, fileFlag = False, path = None):
	if fileFlag:
		if not os.path.exists(path): return "File doesn't exist or path is wrong"
		else:
			with open(path, "r") as fs:
				for row in fs:
					words = row.split()
	if not terminal: return path
	else: return None #show qrCode in terminal 

def cls():
	os.system('cls' if os.name == 'nt' else 'clear')
	return None

def showMenu():
	cases = {1:codeFile,2:decodeFile,3:showStatus,4:showInput,5:terminal,6:exit}
	cls()
	print('-------NUMCODER-------\r\n');
	print("""1.Шифровать файл.\n\r
			2.Дешифровать файл.\r\n
			3.Статистика файла\r\n
			4.Вывод содержимого.\r\n
			5.Терминальный режим.\r\n
			6.Выход\r\n""");
	menuUserInput =  input()
	cases[int(menuUserInput)]()

def getPath():
	print('-------NUMCODER-------\r\n');
	print('Skip this if you have no files to code/decode\r\n');
	readPath = input('Перетащите текстовый файл в терминал: ');
	writePath = os.system()

def codeFile():
	readPath = input('Drag\'n\'drop original file into terminal: ')
	writePath = "{0}/out_coded_file.txt".format(os.environ["TEMP"])
	print ('-------CODE-------\r\ncode '+readPath+' file to num\r\n');
	with open(readPath) as f:
		for line in f:
			codedWords = []
			words = line.split(' ')
			for word in words:
				codeWord = 0
				word = word[::-1].strip(' \t \n \r : , . ! ? ) ( { } [ ] < > ; % & @ " - = + \ | / ~ ')
				index = 0
				for letter in word:
					codeWord = codeWord + (codeLetters[letter] * math.pow(26,index))
					index+=1
				codedWords.append(codeWord)
			outCodedFile = open(writePath,'a')
			outCodedFile.write(str(codedWords).strip('[ ]'))
			outCodedFile.close()
	print('Your file saved into %s' %writePath)

def main(*args,**kwargs):
	if args.__len__() == 0: showMenu()
	else:
		parser = argparse.ArgumentParser()
		parser.add_argument("-code", help = "Type string or drop file you want to place on QR", type = str)
		parser.add_argument("-decode", help = "Drop image file with QR you want to decode", type = str)
		parser.add_argument("-term", help = "Set -term argument if you want to show generated code in terminal", type = bool, default = True)
		parser.parse_args()

if __name__ == "__main__":
	main(sys.argv)