import os
import sys
import subprocess

def parser(proc, match = 2):
	line = proc.stdout.readline()
	if match in line: prinnt('{} FOUND!'.format(match))

def main():
	proc = subprocess.Popen(['x-terminal-emulator','generator.sh'],stdout=subprocess.PIPE)
	while True: parser(proc, '3')
		
if __name__ == '__main__':
	main()
