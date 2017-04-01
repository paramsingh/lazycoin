# host and port for client and tracker
HOST = '127.0.0.1'
PORT = 9997

# redis key prefixes
TRANSACTION_QUEUE_KEY = 'transactions.queue'
BLOCK_KEY_PREFIX = 'chain.block.'
PREV_HASH_KEY = 'prev_hash'
BLOCK_USED_KEY_PREFIX = 'chain.block.used.'
SEND_TRANSACTIONS_QUEUE_KEY = 'send.transactions.queue'

# number of transactions in a block
TRANSACTIONS_IN_BLOCK = 1
