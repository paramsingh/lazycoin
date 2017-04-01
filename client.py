import socket
import funcs
import user
import threading
import json

HOST = '127.0.0.1'
PORT = 9997


def handle_send(sock, User):
	pass

''' Thread receives broadcasted data'''
def handle_receive(sock, User):

	#receiving
	while True:
		message = json.loads(funcs.receive_message(sock))
		if message['type'] == 'Transaction':
			# it is a transaction
		else
			# it is a block request







if __name__ == '__main__':
	
	# the user managing this miner
	User = LazyUser()

	# boradcasting connection to csec
	clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clientSock.connect((HOST,PORT))

	# The receiving thread for this miner
	th = threading.Thread(target = handle_receive, args = [clientSock,User], daemon = True)
	th.start()

	#The Broadcasting thread for this miner
	th = threading.Thread(target = handle_send, args = [clientSock,User], daemon = True)
	th.start()


	'''funcs.send_message(clientSock, "Princu")

	while(True):
		message = funcs.receive_message(clientSock)
		print(message)

	while True: 
		pass
	clientSock.close()'''


