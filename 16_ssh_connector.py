import paramiko
import getpass
import os
import sys

def init_connection(user, password, host):
	return None

def get_credentials():
	u = input('type your username: ')
	p = getpass.getpass('type your password: ')
	h = input('type host IP-address:')
	return u,p,h

def init_tracker(user, ssecret, host, file_log = 'output.log', file_err = 'error.log'):	
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret)
	stdin, stdout, stderr = client.exec_command('')
	while True:
		data_out = stdout.readline()
		data_err = stderr.readline()
		if data_out:
			sys.stdout.write(line)
			sys.stdout.flush()
			with open(file,'a') as out:
	 			out.write('{}'.format(line))
		if line.__len__() == 0 and proc.poll() is not None:
			break 
	client.close()
	return None

def main():
	# file_log = 'output.log'
	# file_err = 'error.log'
	usr, pwd, hst = get_credentials()
	init_tracker(usr,pwd,hst)	
	return None

if __name__:'__main__':
	mani()
