import hashlib
from hashlib import sha256
import json

class Block:
  def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
    self.index = index
    self.transactions = transactions
    self.timestamp = timestamp
    self.previous_hash = previous_hash
    self.nonce = nonce
    self.update_hash()

  def increase_nonce(self):
    self.nonce += 1
    self.update_hash()

  def update_hash(self):
    block_str = json.dumps(self.__dict__, sort_keys=True)
    self.hash = sha256(block_str.encode()).hexdigest()
    return self.hash

import time

class Blockchain:
  def __init__(self):
    self.unconfirmed_transactions = []
    self.chain = []
    self.create_genesis_block()
    
  def create_genesis_block(self):
      block = Block(0, [], time.time(), 0)
      self.chain.append(block)

  def add_transaction(self, transaction):
    self.unconfirmed_transactions.append(transaction)

  def mine(self):
    if not self.unconfirmed_transactions:
      return False
    
    last_block = self.last_block
    new_block = Block(last_block.index + 1, self.unconfirmed_transactions, time.time(),
                      last_block.hash)
    
    self.proof_of_work(new_block)
    self.add_block(new_block)
    self.unconfirmed_transactions = []
    return True

  diff = 3
  def proof_of_work(self, new_block):
      while not new_block.hash.startswith('0' * Blockchain.diff):
        new_block.increase_nonce()

      return new_block.hash

  def add_block(self, new_block):
    if self.last_block.hash != new_block.previous_hash:
      return False
    if not self.is_valid_proof(new_block.hash):
      return False

    self.chain.append(new_block)
    return True

  def is_valid_proof(self, proof):
    return proof.startswith('0' * Blockchain.diff)
  

  @property
  def last_block(self):
    return self.chain[-1]


blockchain = Blockchain()


from flask import Flask, request, redirect

app = Flask(__name__)


btnGoHome = """
<br>
<a href="/">
    <input type="submit" value="Return home"/>
</a>
"""

@app.route('/')
def hello():
    f = open('index.html')
    html = f.read()
    return html
    
@app.route('/print_blockchain')
def print_chain():
    str = ""
    for block in blockchain.chain:
        str += '<br>' + json.dumps(block.__dict__)
    return str + btnGoHome
    
@app.route('/mine')
def mine():
    blockchain.mine()
    return redirect('/')
    
@app.route('/secret_feature')
def secret_feature():
    return "<h1> Hello world! </h1>" + btnGoHome
    
@app.route('/add_transaction', methods=('GET','POST'))
def add_transaction():
    if request.method == 'POST':
        transaction = request.form['transaction']
        blockchain.add_transaction(transaction)
        return "Added transaction: " + transaction + btnGoHome
    if request.method == 'GET':
        f = open('add_transaction.html')
        html = f.read()
        f.close()
        return html
        
    

app.run(debug=True, port=5000)


