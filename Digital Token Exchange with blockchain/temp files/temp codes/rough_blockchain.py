import datetime
import hashlib

def calculate_hash(index, previous_hash, timestamp, data, transactions, nonce):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data) + str(transactions) + str(nonce)
    return hashlib.sha256(value.encode()).hexdigest()

class Block:
    def __init__(self, index, previous_hash, timestamp, data, transactions, nonce, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.transactions = transactions
        self.nonce = nonce
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.difficulty = 4
        self.blockchain = []
        self.transactions = []

    def create_genesis_block(self):
            index=0
            previous_hash = "0"
            timestamp = datetime.datetime.now()
            data = "Genesis Block"
            transactions = self.transactions
            nonce = 0
            hash = calculate_hash(index, previous_hash, timestamp, data, transactions, nonce)
            genesis = Block(index, previous_hash, timestamp, data, transactions, nonce, hash)
            self.blockchain.append(genesis)
    
    def create_block(self, block):
         self.blockchain.append(block)      
    
    def mine(self):
        previous_block = self.blockchain[-1]
        index = int(previous_block.index) + 1
        previous_hash = previous_block.hash
        timestamp = datetime.datetime.now()
        data = f"Block #{int(len(self.blockchain))} data"
        transactions = self.transactions
        nonce = 0
        hash = calculate_hash(index, previous_hash, timestamp, data, transactions, nonce)
        block = Block(index, previous_hash, timestamp, data, transactions, nonce, hash)
        while not block.hash.startswith("0" * self.difficulty):
            nonce += 1
            block.nonce = nonce
            block.hash = calculate_hash(index, previous_hash, timestamp, data, transactions, nonce)
        self.create_block(block)


if __name__ == "__main__":
     blockchain = Blockchain()
     blockchain.create_genesis_block()

     blockchain.mine()
     blockchain.mine()
     blockchain.mine()


     for i in blockchain.blockchain:
          print(i.index)
          print(i.previous_hash)
          print(i.timestamp)
          print(i.data)
          print(i.transactions)
          print(i.nonce)
          print(i.hash)
          print('\n')
          