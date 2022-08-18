import datetime
from hashlib import sha256

class Block:
  def __init__(self, vote_data, previous_hash):
    self.time_stamp = datetime.datetime.now()
    self.vote_data = vote_data
    self.previous_hash = previous_hash
    self.nonce = 0
    self.hash = self.generate_hash()

  def generate_hash(self):
    block_header = str(self.time_stamp) + str(self.vote_data.vote) +str(self.vote_data.name) +str(self.vote_data.email)+str(self.previous_hash) + str(self.nonce)
    block_hash = sha256(block_header.encode())
    return block_hash.hexdigest()

  def print_contents(self):
    print("timestamp:", self.time_stamp)
    print("vote:", self.vote_data)
    print("current hash:", self.generate_hash())
    print("previous hash:", self.previous_hash) 