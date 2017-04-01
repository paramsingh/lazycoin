import funcs
import threading
import queue

HOST = '127.0.0.1'
PORT = 9998

send_lock = threading.Lock()
send_queues = []

def client_receive(client_socket,client_address,q):
	print("connected to " + str(client_socket) + " " )
	with send_lock:
		send_queues.append(q)

	th = threading.Thread(target = send_to_client,args = [client_socket,q],daemon = True)
	th.start()

	while True:
		size = funcs.receive_data(client_socket,5)
		message = funcs.receive_data(client_socket,int(size))

		with send_lock:
			for qu in send_queues:
				if qu != q:
					qu.put(size+message)


def send_to_client(sock,q):
	while True:
		data = q.get()
		if data == None:
			break
		send(sock,data)


def send(sock,data):
	funcs.send_data(sock,data)


if __name__ == '__main__':

	listening_socket = funcs.create_listening_socket(HOST,PORT,100)
	while True:
		print("Waiting")
		client_socket,client_address = listening_socket.accept()
		q = queue.Queue()
		th = threading.Thread(target = client_receive, args = [client_socket,client_address,q], daemon = True)
		th.start()

