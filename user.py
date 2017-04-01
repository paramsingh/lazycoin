import rsa

class User(object):

    def __init__(self):
        self.pub, self.priv = rsa.newkeys(512)

    def sign(self, transaction):
        message = str(transaction)
        signature = rsa.sign(message, self.priv, 'SHA-256')
        return (message, signature)

    def send_coins(self, amount):
        pass
