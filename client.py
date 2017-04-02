import socket
import funcs
import threading
import json
from redis import Redis
import time
import sys
from chain import Transaction, Block
import chain
from user import LazyUser
from config import *
from miner import Miner
import pickle


prev_hash = 'block hash of genesis'
redis_connection = Redis()


def miner_thread(sock, User):
    miner = Miner(redis_connection, User)

    while True:
        print("trying to mine")
        block = miner.mine()
        if block == None:
            redis_connection.set("StopMining","No")
            print("Puzzle solved by other node")
            continue

        print("have a block, broadcasting")
        #funcs.send_message(sock, block.to_redis())
        #funcs.send_object(block)
        serial = pickle.dumps(block)
        print("Serialized block = ")
        print(serial)
        print(json.dumps(block.to_json(), indent=4))
        #print(json.dumps(bl.to_json(),indent = 4))
        funcs.send_message(sock,"Block")
        funcs.send_bytes(sock,serial)


def send_transaction(sock,User):
    while True:
        print("waiting for transaction to be sent")
        payload = json.loads(redis_connection.blpop(SEND_TRANSACTIONS_QUEUE_KEY)[1].decode('utf-8'))
        transaction = Transaction.from_redis(redis_connection, payload)
        print("try to send the received transaction")
        serial = pickle.dumps(transaction)
        funcs.send_message(sock,"Transaction")
        funcs.send_bytes(sock,serial)


def stop_mining():
    redis_connection.set("StopMining","Yes")

def handle_receive(sock, User):
    """ Thread receives broadcasted data """
    while True:

        tp = funcs.receive_message(sock)

        data = funcs.receive_bytes(sock)
        obj = pickle.loads(data)
        if tp == "Transaction":
            # load transaction into a transaction object
            transaction = obj
            # verify transaction and if it is valid, put it into the
            # redis queue of transactions that need to be mined

            # TODO (param): verify if the sender has the money to send
            if transaction.verify():
                print("new transaction added to queue")
                transaction.write_to_redis(redis_connection, TRANSACTION_QUEUE_KEY)
            else:
                print("Invalid transaction received from tracker", file=sys.stderr)
                print("json of transaction: ", file=sys.stderr)
                print(json.dumps(payload, indent=4), file=sys.stderr)

        elif tp == "Block":

            # load block into a block object and verify if it is valid
            # if it is valid, put it into redis and update the prev_hash key
            # and remove the transactions done from the pending transactions queue
            block = obj
            if block.verify():
                # add block to redis
                print("Received block is verified")
                print("Stopping current mining")
                stop_mining()

                key = "{}{}".format(BLOCK_KEY_PREFIX, block.hash)
                print("adding block to key: {}".format(key))
                redis_connection.set(key, json.dumps(block.to_json(), sort_keys=True))

                # make the prev_hash field used by local miner to be the hash of the block
                # we just added
                print("prev hash key set to {}".format(block.hash))
                redis_connection.set(PREV_HASH_KEY, block.hash)

            else:
                print(type(obj))
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
