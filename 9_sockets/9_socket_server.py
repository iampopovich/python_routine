import socket

def init_server():
	sock = socket.socket()
	sock.bind(('',9090))
	sock.listen(1)
	conn, addr = sock.accept() 
	return conn, addr
	

def run_server(connection, address):
	try:
		print('server started...')
		while True:
			data = connection.recv(1024)
			if not data: break
			# if '--help' in data: show_help(conn)
			#conn.send(data.upper())
		# conn.close()
	except Exception as ex:
		conn.close()
		raise ex
	finally:
		conn.close()

def main():
	conn, addr = init_server()
	run_server(conn,addr)

if __name__ == '__main__':
	main()