import paramiko
import getpass
import argparse 
import re

def init_connection(user, secret, host):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret)
	return client

def init_argparser ():
	#regexp for detect level by mask : e.g. [ERROR]/[ERR]/[E]/etc.
	#regexp for detect application by mask : e.g. [LOGWRITER]/[LOGGER]/[LOG]/etc. 
	#return level
	#return app 
	return None

def get_credentials():
	u = input('type your username: ')
	p = getpass.getpass('type your password: ')
	h = input('type host IP-address:')
	return u,p,h

def init_tracker(client, level ='', app = '', file_log = 'output.log', file_err = 'error.log'):	
	try:
		stdin, stdout, stderr = client.exec_command('')
		for data_out in iter(stdout.readline,''):
			with open(file_log,'a') as out:
				out.write('{}'.format(data_out))
		for data_err in iter(stderr.readline,''):
			if data_err != '':
				with open(file_err,'a') as err:
					err.write('{}'.format(data_err))
				break
		client.close()
	except Exception as ex:
		client.close()
		raise ex

def main():
	init_argparser()
	usr, pwd, hst = get_credentials()
	client = init_connection(usr,pwd,hst)
	init_tracker(client)	
	return None

if __name__=='__main__':
	main()
