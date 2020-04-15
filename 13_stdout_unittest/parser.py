import os
import sys
import subprocess
import threading
import unittest

#АССЕРТ true НА if match in line 

def parser(proc, match = 100):
	for line in proc.stdout:
		if match in line:
			print('{} FOUND!'.format(match))


def main():
	# proc = subprocess.Popen(['/bin/sh','-c','{}/generator.sh'.format(os.getcwd())],stdout=subprocess.PIPE, shell = True)
	proc = subprocess.Popen(['/bin/sh','echo 100'],shell=True, stdout = subprocess.PIPE)
	t = threading.Thread(target = parser, args=(proc,'3',), daemon=True)
	t.start()
	t.join()
		
if __name__ == '__main__':
	main()