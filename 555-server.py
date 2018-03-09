#! /usr/local/bin/python3

'''
infinite chill 555 coin
heavily based on the SnakeCoin tutorial series 
available here: https://tinyurl.com/yddx3m84
with a few additions and changes

server usage:

    ./555-server MP00


client usage:

# gets the contents of the current blockchain
    curl localhost:5000/blocks

# requests a transaction to be posted
    curl localhost:5000/txion

'''

from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date
import sys
import threading


node = Flask(__name__)


# local copy of blockchain
blockchain = []
# local stack of transactions
this_nodes_transactions = []
# addresses of peers to talk with
peer_nodes = []
# address of Mining Peer
miner_address = None
# number bof transactions per block
BLOCK_SIZE = 2


# define 555 block structure
class FiveBlock:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash, self.nonce = self.hash_block()
  def hash_block(self):
    # hash block function
    # pow: nonce must be divisible by 55
    # and hash must start with 555
    sha = hasher.sha256()
    nonce=0
    while(1):
        hash_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(nonce)
        sha.update(hash_string.encode('utf-8'))
        result=sha.hexdigest()
        if result[:3]=="555" and nonce%55 == 0:
            break
        nonce+=1
    return result, nonce


# create the genesis block
def create_genesis_block():
  return FiveBlock(0, date.datetime.now(), {
    "transactions": None
  }, "this is the 555 genesis")

# mine the stack of transactions
def mine_block():
  global this_nodes_transactions
  # todo: check if transactions exist to process
  last_block = blockchain[len(blockchain) - 1]
  # Now we can gather the data needed
  # to create the new block
  new_block_data = {
    "transactions": list(this_nodes_transactions)
  }
  new_block_index = last_block.index + 1
  new_block_timestamp = this_timestamp = date.datetime.now()
  last_block_hash = last_block.hash
  # copy transaction list and empty
  transaction_list=this_nodes_transactions[:]
  this_nodes_transactions[:]=[]
  mined_block = FiveBlock(
    new_block_index,
    new_block_timestamp,
    new_block_data,
    last_block_hash
  )
  # todo: reach consensus who won transaction
  blockchain.append(mined_block)
  # let client know transaction was accepted
  # currently just sending the block
  print (json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "transactions": transaction_list,
      "hash": mined_block.hash,
      "nonce": mined_block.nonce,
      "miner_id" : miner_address
  },indent=4) + "\n")


# handle transaction request
@node.route('/txion', methods=['POST'])
def transaction():
  new_txion = request.get_json()
  # todo: check the ledger for valid funds
  # todo: reach consensus that transaction request was valid
  print(this_nodes_transactions)
  this_nodes_transactions.append(new_txion)
  print ("new xaction")
  print ("FROM: {}".format(new_txion['from'].encode('ascii','replace')))
  print ("TO: {}".format(new_txion['to'].encode('ascii','replace')))
  print ("AMOUNT: {}\n".format(new_txion['amount']))
  # if we have reached block size, mine the block
  if len(this_nodes_transactions) == BLOCK_SIZE:
    mining_thread = threading.Thread(target=mine_block,)
    mining_thread.start()
  return "transaction submitted successfully\n"


# handle get blocks request
@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = blockchain
  for i in range(len(chain_to_send)):
    block = chain_to_send[i]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    block_nonce = block.nonce
    chain_to_send[i] = {
      "index": block_index,
      "timestamp": block_timestamp,
      "data": block_data,
      "hash": block_hash,
      "nonce": block_nonce,
    }
  chain_to_send = json.dumps(chain_to_send,indent=4) + "\n"
  return chain_to_send


# mian driver function
def main():
  global this_nodes_transactions,blockchain,peer_nodes,mining
  global miner_address
  # get address of mining peer
  try:
    miner_address = sys.argv[1]
  except:
    print("please supply miner ID")
    print("e.g.\t./555-server MP00")
    sys.exit(1)

  blockchain.append(create_genesis_block())

  mining = True
  node.run()


if __name__ == '__main__':
  main()

