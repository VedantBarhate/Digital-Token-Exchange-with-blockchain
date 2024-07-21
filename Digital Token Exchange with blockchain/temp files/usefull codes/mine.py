import datetime
import hashlib

transactions = [['user1', 'user2', '10', '100', 'time1'],
                ['user2', 'user3', '5', '50', 'time2'],
                ['user3', 'user1', '1', '10', 'time3'],
                ['user3', 'user2', '13', '130', 'time4'],
                ['user4', 'user1', '12', '120', 'time5']]

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

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    def login(self):
        if self.id == 1 and self.name == "user1" and self.password == "0027":
            print("logined")
            return True
        else:
            print("unable to login")
            return False
        
    def mine(self, user, previous_block, data):
        self.user = user
        index = previous_block.index + 1
        timestamp = datetime.datetime().now()
        nonce = 0
        hash = calculate_hash(index, previous_block.hash, timestamp, data, nonce)
        new_block = Block(index, previous_block.hash, timestamp, data, hash, nonce)
        while not new_block.hash.startswith("0000"):
            new_block.nonce += 1
            new_block.hash = calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data, new_block.nonce)
        return new_block
    

user = User(1, "user1", "0027")
login = user.login()
if login:
    user.mine(user, )

    