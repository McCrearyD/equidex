from time import time
import json
import hashlib
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof: int, previous_hash: str = None) -> dict:
        """create a new block in the Blockchain

        proof (int): proof given by the "proof of work" algorithm
        previous_hash (str): hash of previous block
        
        returns (dict): new block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': self.hash(self.last_block) if previous_hash is None else previous_hash
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """creates a new transaction to go into the next mined Block

        sender (str): address of the sender
        recipient (str): address of the recipient
        amount (int): amount

        returns (int): index of the block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self) -> dict:
        return self.chain[-1]

    @staticmethod
    def hash(block: dict) -> str:
        """creates a SHA-256 hash of a Block

        block (dict): block

        return (str)
        """

        # dict should be ordered, to remove inconsistencies
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
        """proof of work algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof

        last_proof (int)

        return (int)
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
                proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """Validates the Proof: Does hash(last_proof, proof) contain 6969 at the end?

        last_proof (int): previous proof
        proof (int): current proof

        return (bool): True if correct, else False
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "6969"

    def register_node(self, address: str):
        """add a new node to the list of nodes

        address (str): address of node ie. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain: list) -> bool:
        """determine if a given blockchain is valid

        chain (list): a blockchain

        return (bool): True if valid, else False
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n---------\n')
            
            # check the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # check proof of work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self) -> bool:
        """this is the consensus algorithm, it resolves conflicts
        by replacing the chain with the longest one in the network

        return (bool): True if our chain was replaced, else False
        """

        neighbors = self.nodes
        new_chain = None

        # look for chains longer than current
        max_length = len(self.chain)

        # grab & verify chains from other nodes in network
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                data = response.json()
                length = data['length']
                chain = data['chain']

                # check if length is longer & chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        return False
