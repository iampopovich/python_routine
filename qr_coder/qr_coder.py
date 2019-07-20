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
# import pyzbar
# import pyqrcoder #прочекай в записях еще 2е либы под qr из окб

class coder:
	def __init__(self):
		pass

class decoder:
	def __init__(self):
		pass
		

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    return None

def showMenu():
	cases = {1:codeFile,2:decodeFile,3:showStatus,4:showInput,5:terminal,6:exit}
	cls()
	print('-------NUMCODER-------\r\n');
	print('1.Шифровать файл.\n\r2.Дешифровать файл.\r\n3.Статистика файла\r\n4.Вывод содержимого.\r\n5.Терминальный режим.\r\n6.Выход\r\n');
	menuUserInput =  input()
	cases[int(menuUserInput)]()

def getPath():
			print('-------NUMCODER-------\r\n');
			print('Skip this if you have no files to code/decode\r\n');
			readPath = input('Перетащите текстовый файл в терминал: ');
			writePath = os.system('c:\\Temp\\out_coded_file.txt' if os.name == 'nt' else '/tmp/out_coded_file.txt')

def codeFile():
	codeLetters = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,
			'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,
			'r':17,'s':18,'t':19,'u':20,'v':21,'w':22,'x':23,'y':24,'z':25}
	codeLettersKyrillic = {'а':0, 'б':1,'в':2,'г':3,'д':4,'е':5,'ж':6,'з':7,
							'и':8,'й':9,'к':10,'л':11,'м':12,'н':13, 'о':14,
							'п':15,'р':16,'с':17,'т':18,'у':19,'ф':20,'х':21,
							'ц':22,'ч':23,'ш':24,'щ':25,'ъ':26,
							'ы':27,'ь':28,'э':29,'ю':30,'я':31}
	cls()
	readPath = input('Drag\'n\'drop original file into terminal: ')
	writePath = '/tmp/outCodedFile.txt' # os.system('c:\\Temp\\out_coded_file.txt' if os.name == 'nt' else '/tmp/out_coded_file.txt')
	cls()
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
			print('Original line is: %s' %line)
			print('Coded line is: %s' %codedWords)
			outCodedFile = open(writePath,'a')
			#outCodedFile.write(line)
			outCodedFile.write(str(codedWords).strip('[ ]'))
			outCodedFile.close()
	print('Your file saved into %s' %writePath)
						
def decodeFile():
	return "Comming soon..."
def showStatus():
	return "Comming soon..."
def showInput():
	return "Comming soon..."
def terminal():
	return "Comming soon..."
def exit():
	return "Comming soon..."

def main(*args,**kwargs):
	if args.__len__() == 0: showMenu()
	else: return None 

if __name__ == "__main__":
	main(sys.argv)