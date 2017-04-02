import socket
import funcs
import threading
import json
from redis import Redis
import time
import sys
from user import LazyUser
from config import HOST, PORT, TRANSACTION_QUEUE_KEY, BLOCK_USED_KEY_PREFIX, BLOCK_KEY_PREFIX, \
    PREV_HASH_KEY, SEND_TRANSACTIONS_QUEUE_KEY
from miner import Miner
import pickle


prev_hash = 'block hash of genesis'
redis_connection = Redis()


def miner_thread(sock, User):
    miner = Miner(redis_connection, User)

    while True:
        print("trying to mine")
        block = miner.mine()
        print("have a block, broadcasting")
        #funcs.send_message(sock, block.to_redis())
        #funcs.send_object(block)
        serial = pickle.dumps(block)
        print("Serialized block = ")
        print(serial)
        #print(json.dumps(bl.to_json(),indent = 4))
        funcs.send_data(sock,serial)


def send_transaction(sock,User):
    while True:
        print("waiting for transaction to be sent")
        payload = json.loads(redis_connection.blpop(SEND_TRANSACTIONS_QUEUE_KEY)[1].decode('utf-8'))
        transaction = Transaction.from_redis(redis_connection, payload)
        print("try to send the received transaction")
        funcs.send_message(sock, transaction)



def handle_receive(sock, User):
    """ Thread receives broadcasted data """
    while True:
        message = funcs.receive_message(sock)
        data = json.loads(message)
        if message['type'] == 'transaction':
            payload = message['payload']
            # load transaction into a transaction object
            transaction = Transaction.from_redis(payload)
            # verify transaction and if it is valid, put it into the
            # redis queue of transactions that need to be mined

            # TODO (param): verify if the sender has the money to send
            if transaction.verify():
                print("new transaction added to queue")
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
                print("adding block")
                redis_connnection.set(key, json.dumps(payload))

                # store in redis that this block hasn't been used yet
                redis_connnection.set("{}{}".format(BLOCK_USED_KEY_PREFIX, block.hash), '0')

                # make the prev_hash field used by local miner to be the hash of the block
                # we just added
                print("prev hash key set to {}".format(block.hash))
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
    rec_thread = threading.Thread(target = handle_receive, args = [clientSock,User], daemon = True)
    rec_thread.start()

    # The broadcasting thread for this client
    broadcast_thread = threading.Thread(target = miner_thread, args = [clientSock,User], daemon = True)
    broadcast_thread.start()

    th = threading.Thread(target = send_transaction, args = [clientSock,User], daemon = True)
    th.start()

    while True:
        time.sleep(3)


    clientSock.close()
