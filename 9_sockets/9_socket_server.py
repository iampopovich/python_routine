import sockets

def init_server():
	sock = sockets.socket()
	sock.bind('',9090)
	sock.listen(1)
	return socket.accept()

def run_server(connection, address):
	while True:
		data = con.recv(1024)
		if not data: break
		if '--help' in data: show_help(conn)
		#conn.send(data.upper())
	conn.close()

def main():
	conn, addr = init_server()
	run_server()

if __name__ == '__main__':
	main()