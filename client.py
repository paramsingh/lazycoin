import socket
import funcs
import user
import threading
import json
import redis

HOST = '127.0.0.1'
PORT = 9997

# redis connection
rc = redis.StrictRedis(host='localhost', port=6379, db=0)

prev_hash = 'block hash of genesis'


def miner_thread(sock, User):
	miner = Miner()

	while True:
		block = miner.mine()
		funcs.send_message(sock,json.dumps(block))

def send_transaction(sock,User):
	pass


''' Thread receives broadcasted data'''
def handle_receive(sock, User):
	pass



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
	th = threading.Thread(target = miner_thread, args = [clientSock,User], daemon = True)
	th.start()

	th = threading.Thread(target = send_transaction, args = [clientSock,User], daemon = True)
	th.start()


	'''funcs.send_message(clientSock, "Princu")

	while(True):
		message = funcs.receive_message(clientSock)
		print(message)

	while True: 
		pass
	clientSock.close()'''


