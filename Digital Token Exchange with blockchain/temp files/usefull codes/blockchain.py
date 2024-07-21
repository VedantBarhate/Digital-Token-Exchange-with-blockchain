import hashlib
import datetime

def calculate_hash(index, previous_hash, timestamp, data, nonce):
    block_data = f"{index}{previous_hash}{timestamp}{data}{nonce}"
    return hashlib.sha256(block_data.encode()).hexdigest()

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

class Blockchain:
    def __init__(self):
        self.blockchain = [self.create_genesis_block]

    def create_genesis_block(self):
        index=0
        previous_hash = "0"
        timestamp = datetime.datetime().now()
        data = "Genesis Block"
        nonce = 0
        hash = calculate_hash(index, previous_hash, timestamp, data, nonce)
        return Block(index, previous_hash, timestamp, data, hash, nonce)
    
    def previous_block(self):
        return self.blockchain[-1]

    # def create_new_block(self, previous_block, data):
    #     index = previous_block.index + 1
    #     timestamp = datetime.datetime().now()
    #     nonce = 0
    #     hash = calculate_hash(index, previous_block.hash, timestamp, data, nonce)
    #     new_block = Block(index, previous_block.hash, timestamp, data, hash, nonce)
    #     while not new_block.hash.startswith("0000"):
    #         new_block.nonce += 1
    #         new_block.hash = calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data, new_block.nonce)
    #     return new_block


        





