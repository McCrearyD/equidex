from time import time
import hashlib



class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self, proof, previous_hash=None):
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
            'previous_hash': previous_hash or self.hash(self.last_block),
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
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """creates a SHA-256 hash of a Block

        block (dict): block

        return (str)
        """

        # dict should be ordered, to remove inconsistencies
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
