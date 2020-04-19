import socket

def init_server():
	sock = socket.socket()
	sock.bind(('',9191))
	sock.listen(1)
	conn, addr = sock.accept() 
	print('server started...')
	while True:
		data = connnection.recv(1024)
		if not data: break
		if '--help' in data: show_help(conn)
		#conn.send(data.upper())
	conn.close()

def main():
	init_server()

if __name__ == '__main__':
	main()