from redis import Redis
import time
from config import TRANSACTION_QUEUE_KEY, BLOCK_USED_KEY_PREFIX, BLOCK_KEY_PREFIX, PREV_HASH_KEY
from chain import Transaction, Block


class Miner(object):

    def __init__(self, redis_connection, user):
        self.r = redis_connection
        self.user = user

    def mine(self):
        """ Looks in redis for transactions and mines them to find the answer to the puzzle
        """

        prev_hash = self.r.get(PREV_HASH_KEY)
        block = Block(prev_hash)

        # wait to fill the block with transactions
        while not block.full():
            # blocking pop from transaction key
            transaction = Transaction.from_json(self.r.blpop(TRANSACTION_QUEUE_KEY))
            block.add_transaction(transaction)

        # create a new transaction that creates a lazycoin and gives it to the user
        create = Transaction(
                prev_hash=prev_hash,
                transaction_type='CREATE',
                sender=None,
                receiver=self.user.pub,
            )

        # sign this transaction and add the signature to the transaction
        msg, sign = self.user.sign(create)
        create.add_signature(sign)

        block.add_transaction(create)

        nonce = self.solve_puzzle(block)

        block.add_nonce(nonce)
        return block

    def solve_puzzle(self, block):
        print("solving puzzle")
        return 0

