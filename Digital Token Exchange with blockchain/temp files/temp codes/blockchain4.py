import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

    def calculate_hash(self):
        data_string = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.data) + str(self.nonce)
        return hashlib.sha256(data_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Adjust the difficulty by changing the number of leading zeros in the hash

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def mine_block(self, user):
        data = f"Reward for {user}"
        index = len(self.chain)
        timestamp = time.time()
        previous_hash = self.get_latest_block().hash
        nonce = 0
        new_block = Block(index, previous_hash, timestamp, data, "")

        while not new_block.hash.startswith("0" * self.difficulty):
            nonce += 1
            new_block.nonce = nonce
            new_block.hash = new_block.calculate_hash()

        print(f"Block mined by {user}: {new_block.hash}")
        self.add_block(new_block)

if __name__ == "__main__":
    # Example usage
    my_coin = Blockchain()

    # Mining by users
    user1 = "Alice"
    user2 = "Bob"

    my_coin.mine_block(user1)
    my_coin.mine_block(user2)

    # Display the blockchain
    for block in my_coin.chain:
        print(f"Block #{block.index} | Hash: {block.hash} | Data: {block.data} | Mined by: {user1 if block.data.startswith('Reward') else user2}")
