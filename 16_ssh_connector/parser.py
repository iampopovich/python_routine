import paramiko
import getpass
import argparse 
import re

class Parser:
	def __init__(self, host = None, user = None, secret = None, level = None, app = None):
		self.host = None
		self.user = None
		self.secret = None
		self.conn = None
		self.level = None
		self.app = None
		self.file_log = None
		self.file_err = None
		self.ssh_command = None
		self.set_file_log()
		self.set_file_error() 

	def init_connection(self):
		try:
			if all([self.host,self.user,self.secret]):
				client = paramiko.SSHClient()
				client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				client.connect(hostname=self.host, username=self.user, password=self.secret)
				self.conn = client
			else:
				print('Fill all credentials before...')
				return None
		except Exception as ex:
			return ex

	def set_level(self, level=''):
		self.level = level

	def set_application(self, app =''):
		self.app = app

	def set_file_log(self, file_log='output.log'):
		self.file_log = file_log

	def set_file_error(self, file_err = 'error.log'):
		self.file_err = file_err

	def set_command(self):
		self.ssh_command = input('type command: ')

	def set_credentials(self):
		self.user = input('type your username: ')
		self.secret = getpass.getpass('type your password: ')
		self.host = input('type host IP-address: ')
		
	def init_tracker(self, levels = None, apps = None):	
		try:
			stdin, stdout, stderr = self.conn.exec_command(self.ssh_command)
			for data_out in iter(stdout.readline,''):
				data_out = re.sub(r'\[[0-9]{2};[0-9]{1,2}[a-zA-Z]{1}','',data_out)
				with open(self.file_log,'a') as out:
					out.write('{}'.format(data_out))
			for data_err in iter(stderr.readline,''):
				if data_err != '':
					with open(self.file_err,'a') as err:
						err.write('{}'.format(data_err))
					break
			self.conn.close()
		except Exception as ex:
			self.conn.close()
			raise ex

def init_argparser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-lvl', metavar='LEVEL', type = str, required = False) #e.g. [ERROR]/[ERR]/[E]/etc.
	parser.add_argument('-app', metavar = 'APP', type = str, required = False) #e.g. [LOGWRITER]/[LOGGER]/[LOG]/etc. 
	return parser
	
def main():
	argaparser = init_argparser()
	args = argaparser.parse_args()
	parser = Parser()
	parser.set_credentials() #если кваргс пустой - то инпутим, если заполненный - то берем из кваргс
	parser.set_command()
	parser.init_connection()
	if args['level']:
		parser.set_level(args['level'])
	if args['app']:
		parser.set_app(args['app'])
	parser.init_tracker()

if __name__=='__main__':
	main()
