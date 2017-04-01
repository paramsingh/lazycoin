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
	if(len(s)<size):
		s = '0'*(size-len(s))+s
	return s

def create_listening_socket(host,port,size):
	listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	listening_socket.bind((host,port))
	listening_socket.listen(100)
	return listening_socket




def receive_message(sock,size):
	msg = receive_data(sock,size)
	msg = msg.decode('utf-8')
	return msg


def send_message(sock,uno,message,sig = 999):
	message = message.encode('utf-8')
	header = create_header(uno,sig,len(message))
	message = header+message
	send_data(sock,message)