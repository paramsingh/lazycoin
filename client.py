import socket
import funcs
import user
import threading
import json
from redis import Redis
import time
import sys

HOST = '127.0.0.1'
PORT = 9997
TRANSACTION_QUEUE_KEY = 'transactions.queue'
BLOCK_KEY_PREFIX = 'chain.block.'
PREV_HASH_KEY = 'prev_hash'
BLOCK_USED_KEY_PREFIX = 'chain.block.used.'

prev_hash = 'block hash of genesis'


def miner_thread(sock, User):
	miner = Miner()

	while True:
		block = miner.mine()
		funcs.send_message(sock,json.dumps(block))


def send_transaction(sock,User):
	pass


def handle_receive(sock, User):
    """ Thread receives broadcasted data """
    while True:
        message = funcs.receive_message(sock)
        data = json.loads(message)
        if message['type'] == 'transaction':
            payload = message['payload']
            # load transaction into a transaction object
            transaction = Transaction.from_json(payload)
            # verify transaction and if it is valid, put it into the
            # redis queue of transactions that need to be mined

            # TODO (param): verify if the sender has the money to send
            if transaction.verify():
                redis_connection.rpush(TRANSACTION_QUEUE_KEY, json.dumps(payload))
            else:
                print("Invalid transaction received from tracker", file=sys.stderr)
                print("json of transaction: ", file=sys.stderr)
                print(json.dumps(payload, indent=4), file=sys.stderr)

        elif message['type'] == 'block':
            payload = message['payload']
            # load block into a block object and verify if it is valid
            # if it is valid, put it into redis and update the prev_hash key
            # and remove the transactions done from the pending transactions queue
            block = Block.from_json(payload)
            if block.verify():
                # add block to redis
                key = "{}{}".format(BLOCK_KEY_PREFIX, block.hash)
                redis_connnection.set(key, json.dumps(payload))

                # store in redis that this block hasn't been used yet
                redis_connnection.set("{}{}".format(BLOCK_USED_KEY_PREFIX, block.hash), '0')

                # make the prev_hash field used by local miner to be the hash of the block
                # we just added
                redis_connection.set(PREV_HASH_KEY, block.hash)

                # TODO (param): remove pending transactions
            else:
                print("Invalid block received from tracker", file=sys.stderr)
                print("json of transaction: ", file=sys.stderr)
                print(json.dumps(payload, indent=4), file=sys.stderr)


if __name__ == '__main__':
	# the user managing this client
    # TODO (param): manage this guy's stuff that should be in redis
	User = LazyUser()

	# boradcasting connection to tracker
	clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clientSock.connect((HOST,PORT))

	# The receiving thread for this client
	th = threading.Thread(target = handle_receive, args = [clientSock,User], daemon = True)
	th.start()

	# The broadcasting thread for this client
	th = threading.Thread(target = miner_thread, args = [clientSock,User], daemon = True)
	th.start()

	th = threading.Thread(target = send_transaction, args = [clientSock,User], daemon = True)
	th.start()

	clientSock.close()
