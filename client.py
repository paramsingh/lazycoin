import socket
import funcs

HOST = '127.0.0.1'
PORT = 9998

if __name__ == '__main__':
	clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clientSock.connect((HOST,PORT))


	msg = "Princu"
	data = msg.encode('utf-8')
	size = funcs.nDigit(str(len(data)),5)
	print('size = ', size)
	size = size.encode('utf-8')
	funcs.send_data(clientSock,size+data)

	while(True):
		size = funcs.receive_data(clientSock,5)
		message = funcs.receive_data(clientSock,int(size))
		print(message.decode('utf-8'))

	while True: 
		pass
	clientSock.close()


