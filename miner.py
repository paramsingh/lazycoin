from redis import Redis
import time
from config import TRANSACTION_QUEUE_KEY, BLOCK_USED_KEY_PREFIX, BLOCK_KEY_PREFIX, PREV_HASH_KEY
from chain import Transaction, Block
import json


class Miner(object):

    def __init__(self, redis_connection, user):
        self.r = redis_connection
        self.user = user

    def mine(self):
        """ Looks in redis for transactions and mines them to find the answer to the puzzle
        """
        print("Mining")

        prev_hash = self.r.get(PREV_HASH_KEY)
        block = Block(prev_hash)

        # wait to fill the block with transactions
        while not block.full():
            print("Searching for transactions to fill the block")
            # blocking pop from transaction key
            transaction = Transaction.from_redis(self.r, json.loads(self.r.blpop(TRANSACTION_QUEUE_KEY)[1].decode('utf-8')))
            print("found a transaction, adding it to block")
            block.add_transaction(transaction)

        # create a new transaction that creates a lazycoin and gives it to the user
        print("Block is full, now add a create transaction")
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
        print(json.dumps(block.to_json(), indent=4))
        return block

    def solve_puzzle(self, block):
        print("solving puzzle")
        return 0

