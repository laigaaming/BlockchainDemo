# -*- coding: UTF-8 -*-
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        # Create the genesis block
        self.new_block(previous_hash = 1, proof = 100)

    def new_block(self, proof, previous_hash = None):
        '''
        生成新块
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) Hash of previous Block
        :return: New Block
        '''

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        '''
        生成新交易信息，信息将加入到下一个待挖的区块中
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        '''

        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            }
        )
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        '''
        生成块的 SHA-256 hash值
        :param block:
        :return:
        '''

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        '''
        简单的工作量证明:
        - 查找一个 p' 使得 hash(pp') 以4个0开头
        - p 是上一个块的证明, p' 是当前的证明
        :param last_proof:
        :return:
        '''

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        验证证明: 是否hash(last_proof, proof)以4个0开头?
        :param last_proof: Previous Proof
        :param proof: Current Proof
        :return: True if correct, False if not.
        '''

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

# Instantiate our Node
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
blockchain = Blockchain()
@app.route('/mine', methods = ['GET'])
def mine():
    return 'We will mine a new Block'
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return 'We will add a new transaction'
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)