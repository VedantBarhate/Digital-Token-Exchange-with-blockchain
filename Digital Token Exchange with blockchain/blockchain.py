import hashlib
import datetime
from mysqlessentials import *

def calculate_hash(index, previous_hash, timestamp, data, nonce):
    block_data = f"{index}{previous_hash}{timestamp}{data}{nonce}"
    return hashlib.sha256(block_data.encode()).hexdigest()

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.hash = hash
        self.nonce = nonce

class Blockchain:
    def create_genesis_block(self):
        my_cursor.execute("SELECT COUNT(*) FROM blockchain_db;")
        result = my_cursor.fetchall()[0][0]
        if result==0:
            index=0
            previous_hash = "0"
            timestamp = datetime.datetime.now()
            transaction = "GenesisBlock"
            nonce = 0
            hash = calculate_hash(index, previous_hash, timestamp, transaction, nonce)
            block = Block(index, previous_hash, timestamp, transaction, hash, nonce)
            info=str(block.index)+"&"+str(block.previous_hash)+"&"+str(block.timestamp)+"&"+str(block.transactions)+"&"+str(block.hash)+"&"+str(block.nonce)
            my_cursor.execute(f'INSERT INTO blockchain_db VALUES ("{block.index}", "{info}", "BROKER", "{timestamp}");')
            my_conn.commit()
        else:
            pass
    
    def previous_block_data(self):
        my_cursor.execute("SELECT * FROM blockchain_db;")
        result = my_cursor.fetchall()
        last = result[-1][1]
        return last
    
    def add_to_chain(self, block, info, miner, time):
        my_cursor.execute(f'INSERT INTO blockchain_db VALUES ("{block.index}", "{info}", "{miner}", "{time}");')