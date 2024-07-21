import hashlib
import time
import sqlite3

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode()).hexdigest()

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", calculate_hash(0, "0", time.time(), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

def initialize_database():
    connection = sqlite3.connect("blockchain.db")
    cursor = connection.cursor()

    # Create a table to store blocks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            index INTEGER,
            previous_hash TEXT,
            timestamp REAL,
            data TEXT,
            hash TEXT
        )
    ''')

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

def insert_block_into_database(block):
    connection = sqlite3.connect("blockchain.db")
    cursor = connection.cursor()

    # Insert block data into the database
    cursor.execute('''
        INSERT INTO blocks (index, previous_hash, timestamp, data, hash)
        VALUES (?, ?, ?, ?, ?)
    ''', (block.index, block.previous_hash, block.timestamp, block.data, block.hash))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Example usage
initialize_database()
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Add blocks to the blockchain and store them in the database
num_blocks_to_add = 10

for i in range(1, num_blocks_to_add + 1):
    new_data = f"Block #{i} data"
    new_block = create_new_block(previous_block, new_data)
    blockchain.append(new_block)
    previous_block = new_block

    # Store the block in the database
    insert_block_into_database(new_block)

    print(f"Block #{i} has been added to the blockchain and stored in the database!")
    print(f"Hash: {new_block.hash}\n")
