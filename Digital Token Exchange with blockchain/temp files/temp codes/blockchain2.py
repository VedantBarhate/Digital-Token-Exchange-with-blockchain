import hashlib
import time
import requests
from uuid import uuid4

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:6] == '000000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = str(block).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True

    def register_node(self, address):
        self.nodes.add(address)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block['previous_hash'] != self.hash(last_block):
                return False

            proof = block['proof']
            previous_proof = last_block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] != '0000':
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbors:
            # Assume nodes share their blockchain as a Python list
            remote_chain = requests.get(f'http://{node}/chain').json()['chain']

            if len(remote_chain) > max_length and self.valid_chain(remote_chain):
                max_length = len(remote_chain)
                new_chain = remote_chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def create_transaction(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

def mine():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # blockchain.create_transaction(sender="0", recipient=node_identifier, amount=1)
    block = blockchain.create_block(proof, previous_hash)
    print('Congratulations, you just mined a block!')
    print(f'Index: {block["index"]}')
    print(f'Timestamp: {block["timestamp"]}')
    print(f'Proof: {block["proof"]}')
    print(f'Previous Hash: {block["previous_hash"]}')
    print(f'Transactions: {block["transactions"]}')
    print('\n')

def new_transaction():
    sender = input('Enter sender: ')
    recipient = input('Enter recipient: ')
    amount = float(input('Enter amount: '))
    index = blockchain.create_transaction(sender, recipient, amount)
    print(f'Transaction will be added to Block {index}\n')

def display_chain():
    print('Current Blockchain:')
    print(blockchain.chain)
    print('\n')

def register_nodes():
    nodes = input('Enter nodes (comma-separated): ').split(',')
    for node in nodes:
        blockchain.register_node(node.strip())
    print('New nodes have been added\n')

def resolve_conflicts():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        print('Our chain was replaced')
        print('New Blockchain:')
        print(blockchain.chain)
    else:
        print('Our chain is authoritative\n')

if __name__ == '__main__':
    blockchain = Blockchain()
    node_identifier = str(uuid4()).replace('-', '')

    print(f"Node ID: {node_identifier}")

    while True:
        print('Choose an action:')
        print('1. Mine a new block')
        print('2. Create a new transaction')
        print('3. Display current blockchain')
        print('4. Register nodes')
        print('5. Resolve conflicts')
        print('6. Quit')

        choice = input('Enter your choice: ')

        if choice == '1':
            mine()
        elif choice == '2':
            new_transaction()
        elif choice == '3':
            display_chain()
        elif choice == '4':
            register_nodes()
        elif choice == '5':
            resolve_conflicts()
        elif choice == '6':
            break
        else:
            print('Invalid choice. Please try again.\n')
