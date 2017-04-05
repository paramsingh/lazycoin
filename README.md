# Blockchain for lazycoin

An implementation of a blockchain used to manage transactions in a new cryptocurrency called lazycoin.

The blockchain uses RSA public and private keys for signing transactions and SHA-256 for hashing transactions and blocks.

Signed transactions and blocks are broadcasted as objects using pickle over the network.

The blockchain is completely autonomous except for a tracker for broadcasting objects among peers. 

Redis is used to maintain the block chain in all peers and hash pointers to verify transaction.

Miners compete over a Hash Puzzle which is made using SHA-256 Hash digest of outstanding transactions to find the nonce.

This was a project for a 2 day Hackathon that took place in NITH during Nimbus 2017.


## Authors

LazyLeaves

* [Param Singh](https://github.com/paramsingh)
* [Abhishek Rastogi](https://github.com/Princu7)
* [Shikhar Srivastava](https://github.com/shikharsrivastava)
