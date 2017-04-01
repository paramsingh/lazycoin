import socket
import funcs

HOST = '127.0.0.1'
PORT = 9997

if __name__ == '__main__':
	clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clientSock.connect((HOST,PORT))

	funcs.send_message(clientSock, "Princu")

	while(True):
		message = funcs.receive_message(clientSock)
		print(message)

	while True: 
		pass
	clientSock.close()


