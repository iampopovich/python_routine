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

def init_tracker():
	return None

def main():
	usr, pwd, hst = get_credentials()
	return None

if __name__:'__main__':
	mani()
