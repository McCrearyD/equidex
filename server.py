from flask import Flask, jsonify, request
from uuid import uuid4

from blockchain import Blockchain


# setup
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # receive reward for finding proof
    # sender is '0' to signify this node found a new coin
    blockchain.new_transaction(
        sender='0',
        recipient=node_identifier,
        amount=1
    )

    # add Block to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash=previous_hash)

    response = {
        'message': 'new block forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # validate inputs
    required = ('sender', 'recipient', 'amount')
    if not all(k in values for k in required):
        return 'missing values', 400

    # create new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'transaction will be added to block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
