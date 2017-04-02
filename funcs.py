import socket

def send_data(sock,data):
	sock.sendall(data)



def receive_data(sock,size = 4096):
	data = bytes()
	while size:
		recv = sock.recv(size)
		if not recv:
			raise ConnectionError()
		data += recv
		size -= len(recv)
	return data

def nDigit(s,size):
	s = str(s)
	if(len(s)<size):
		s = '0'*(size-len(s))+s
	return s

def send_bytes(sock,data)
	size = nDigit(len(data),5).encode('utf-8')
	sendall(size+data)

def receive_bytes(sock,data)
	size = receive_data(sock,5).decode('utf-8')
	data = receive_data(sock,int(size))
	return data

def create_listening_socket(host,port,size):
	listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	listening_socket.bind((host,port))
	listening_socket.listen(100)
	return listening_socket


def receive_message(sock):
	size = receive_data(sock,5).decode('utf-8')
	msg = receive_data(sock,int(size)).decode('utf-8')
	return msg


def send_message(sock,message):
	message = message.encode('utf-8')
	size = nDigit(len(message),5).encode('utf-8')
	message = size+message
	send_data(sock,message)