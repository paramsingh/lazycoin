from redis import Redis
import rsa
from hashlib import sha256
import json

TRANSACTIONS_IN_BLOCK = 1

class Transaction(object):

    ''' Constructor for creating new transaction'''
    def __init__(self, prev_hash, transaction_type, sender, receiver, signature):
        self.prev_hash = prev_hash
        self.transaction_type = transaction_type
        self.sender = sender
        self.receiver = receiver
        self.signature = signature
        self.message = self.to_str()
        self.hash = sha256(self.message.encode('utf-8')).hexdigest()

    def to_str(self):
        return json.dumps(self.__dict__)

    ''' Verifies the signature on transaction'''
    def verify(self):
        message = self.to_str()
        try:
            rsa.verify(message, self.signature, self.sender)
        except VerificationError:
            print("Verification failed", file=sys.stderr)
            return False

        return True

    @classmethod
    def from_json(cls, payload):
        return cls(
            prev_hash=payload['prev_hash'],
            transaction_type=payload['transaction_type'],
            sender=payload['sender'],
            receiver=payload['receiver'],
            signature=payload['signature'],
        )

class Block(object):

    def __init__(self, prev_hash):
        self.prev_hash = prev_hash
        self.transactions = []

    def add_transaction(self, transaction):
        if len(self.transactions) < TRANSACTIONS_IN_BLOCK:
            self.transactions.append(transaction)
            return True
        else:
            return False

    def add_create_transaction(self, transaction):
        """ adds a transaction that creates lazycoins """
        self.transactions.append(transaction)

    def add_nonce(self, nonce):
        self.nonce = nonce
        # now get the hash also
        self.hash = sha256(json.dumps(self.__dict__).encode('utf-8')).hexdigest()

    @classmethod
    def from_json(cls, payload):
        obj = cls(payload['prev_hash'])
        for transaction in payload['transactions']:
            obj.transactions.append(Transaction.from_json(transaction))
        obj.add_nonce(payload['nonce'])
        return obj


if __name__ == '__main__':
    t = Transaction('fdjasklfasd', 'fasdjklajsdf', 'fdsjk', 'fdjsak', 'fdjskl')
    print(t.to_str())
