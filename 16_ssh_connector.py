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

def init_tracker(user, secret, host, file_log = 'output.log', file_err = 'error.log'):	
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret)
	stdin, stdout, stderr = client.exec_command('')
	for data_out in iter(stdout.readline,''):
		data = data_out.decode('utf-8')
		if data == '': break
		with open(file_log,'a') as out:
			out.write('{}'.format(data))
	for data_err in iter(stderr.readline,''):
			data = data_err.decode('utf-8')
			if data_err != '':
				with open(file_err,'a') as err:
					err.write('{}'.format(data_err.decode('utf-8')))
				break
	client.close()
	return None

def main():
	usr, pwd, hst = get_credentials()
	init_tracker(usr,pwd,hst)	
	return None

if __name__=='__main__':
	main()
