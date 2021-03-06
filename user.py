import rsa
import json

class LazyUser(object):

    def __init__(self):
        self.pub, self.priv = rsa.newkeys(512)

    def sign(self, transaction):
        message = json.dumps(transaction.to_dict(), sort_keys=True).encode('utf-8')
        signature = rsa.sign(message, self.priv, 'SHA-256')
        return (message, signature)
