from redis import Redis
import rsa
from hashlib import sha256
import json


class Transaction(object):

    def __init__(self, prev_hash, transaction_type, sender, receiver):
        """ Constructor for creating new transaction
        """
        self.prev_hash = prev_hash
        self.transaction_type = transaction_type
        self.sender = sender
        self.receiver = receiver


    def add_signature(self, signature):
        """ Add signature to the transaction """
        self.signature = signature

    @property
    def hash(self):
        return sha256(self.to_dict().encode('utf-8')).hexdigest()

    def to_dict(self):
        """
        Converts the transaction data into a serializable json format.
        """
        return {
            'prev_hash': self.prev_hash,
            'transaction_type': self.transaction_type,
            'sender': self.sender,
            'receiver': self.receiver,
        }


    def to_redis(self):
        """
        Converts the entire transaction into a json format that can be put into redis
        """

        return {
            'signature': self.signature,
            'data': self.to_dict(),
        }


    def verify(self):
        """ Verifies the signature of transaction
        """
        try:
            rsa.verify(self.message, self.signature, self.sender)
        except VerificationError:
            print("Verification failed", file=sys.stderr)
            return False

        return True


    @classmethod
    def from_redis(cls, payload):
        """ Factory to create a Transaction object from redis
        """
        obj = cls(
            prev_hash=payload['data']['prev_hash'],
            transaction_type=payload['data']['transaction_type'],
            sender=payload['data']['sender'],
            receiver=payload['data']['receiver'],
        )
        obj.add_signature(payload['signature'])
        return obj


class Block(object):

    def __init__(self, prev_hash):
        self.prev_hash = prev_hash
        self.transactions = []


    def full(self):
        return len(self.transactions) >= TRANSACTIONS_IN_BLOCK


    def add_transaction(self, transaction):
        self.transactions.append(transaction)


    def to_json(self):
        payload = {
            'nonce': self.nonce,
            'prev_hash': self.prev_hash,
            'transactions': [],
        }
        for t in self.transactions:
            transactions.append(t.to_redis())
        return payload


    def add_nonce(self, nonce):
        self.nonce = nonce


    @property
    def hash(self):
        return sha256(json.dumps(self.to_json()).encode('utf-8')).hexdigest()


    @classmethod
    def from_json(cls, payload):
        obj = cls(payload['prev_hash'])
        for transaction in payload['transactions']:
            obj.transactions.append(Transaction.from_json(transaction))
        obj.add_nonce(payload['nonce'])
        return obj

    def verify(self):
        return self.nonce == 0


if __name__ == '__main__':
    pass
