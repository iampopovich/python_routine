import socket

def init_client():
	sock = socket.socket()
	sock.connect(('',9191))
	
	while True:
		info = input('write something... ')
		if info == 'exit': break
		else:
			sock.send(info)
			data = sock.recv(1024)

	sock.close()

def main():
	init_client()

if __name__:=='__main__':
	main()