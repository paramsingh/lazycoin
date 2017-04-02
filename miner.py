from redis import Redis
import time
from config import *
from chain import Transaction, Block
import json
from random import randint
import hashlib

class Miner(object):

    def __init__(self, redis_connection, user):
        self.r = redis_connection
        self.user = user

    def stop_mining(self):
        val = self.r.get("StopMining")
        if val:
            val = val.decode('utf-8')
        if val == 'Yes':
            return True
        else:
            return False

    def mine(self):
        """ Looks in redis for transactions and mines them to find the answer to the puzzle
        """
        print("Mining")

        prev_hash = self.r.get(PREV_HASH_KEY)
        if prev_hash:
            prev_hash = prev_hash.decode('utf-8')

        block = Block(prev_hash)


        # wait to fill the block with transactions
        while not block.full():
            # in between mining
            if self.stop_mining():
                print("Someone mined the coins")
                l = len(block.transactions)
                left = TRANSACTIONS_IN_BLOCK - l
                for _ in range(left):
                    self.r.blpop(TRANSACTION_QUEUE_KEY)
                return None

            print("Searching for transactions to fill the block")
            # blocking pop from transaction key
            transaction = Transaction.from_redis(self.r, json.loads(self.r.blpop(TRANSACTION_QUEUE_KEY)[1].decode('utf-8')))
            print("found a transaction, adding it to block")
            block.add_transaction(transaction)

        # create a new transaction that creates a lazycoin and gives it to the user
        print("Block is full, now add a create transaction")
        print("Prev hash = ", prev_hash)
        create = Transaction(
                prev_hash=prev_hash,
                transaction_type='CREATE',
                sender=self.user.pub,
                receiver=self.user.pub,
            )

        # sign this transaction and add the signature to the transaction
        print("signing transaction")
        msg, sign = self.user.sign(create)
        create.add_signature(sign)

        print("adding transaction")
        block.add_transaction(create)

        print("finding nonce")
        nonce = self.solve_puzzle(block)

        block.add_nonce(nonce)
        print("block done")

        if self.stop_mining():
            print("stopping mining")
            return None

        return block

    def solve_puzzle(self, block):

        print("solving puzzle")
        acc = ''
        for t in block.transactions:
            print("hash: ", str(t.hash))
            acc += str(t.hash)
        print("accumulate:", acc)


        while True:
            nonce = str(randint(1,10**9))
            if int(hashlib.sha256((nonce+acc).encode('utf-8')).hexdigest()[0:6],16) < GAMER_BAWA:
                print("val:", int(hashlib.sha256((nonce+acc).encode('utf-8')).hexdigest()[0:4],16))
                print("nonce:", nonce)
                return nonce
