#! /usr/local/bin/python3

'''
infinite chill 555 coin

test usage:
    ./555-coin num_coins_to_test

'''

import hashlib as hasher
import datetime as date
import sys

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

# wrapper function that returns a block object
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "block number:" + str(this_index)
    this_hash = last_block.hash
    return FiveBlock(this_index, this_timestamp, this_data, this_hash)


# create the genesis block
def create_genesis_block():
  return FiveBlock(0, date.datetime.now(), {
    "transactions": None
  }, "this is the 555 genesis")


def test_code(num_of_blocks_to_add=20):
    # create blockchain and add the genesis block
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]
    # test adding blocks to the chain
    for i in range(0, num_of_blocks_to_add):
      block_to_add=next_block(previous_block)
      blockchain.append(block_to_add)
      previous_block = block_to_add
      # just show the first ten and last ten of hash
      prev_hash=block_to_add.previous_hash[:10]+"..."+block_to_add.previous_hash[-10:]
      curr_hash=block_to_add.hash[:10]+"..."+block_to_add.hash[-10:]
      nonce=block_to_add.nonce
      index=block_to_add.index
      print('{:15s}'.format('block number:'),'{:10d}'.format(index))      
      print('{:15s}'.format('nonce:'),'{:10d}'.format(nonce))
      print('{:15s}'.format('previous hash:'),'{:23s}'.format(prev_hash))
      print('{:15s}'.format('curr hash:'),'{:23s}'.format(curr_hash))
      print()


def main():
    try:
        test_num=int(sys.argv[1])
        test_code(test_num)
    except:
        print("error.")
        sys.exit(1)


if __name__ == '__main__':

    main()

