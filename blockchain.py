#imports the Block class from block.py
from block import Block
import random
from voteInfo import voteInfo

class Blockchain:
  def __init__(self):
    self.chain = []
    self.all_vote_data = []
    self.genesis_block()
    self.done_signal = 0
    self.difficulty = 6
#First block in the chain
  def genesis_block(self):
    vote_data = voteInfo("","","")
    genesis_block = Block(vote_data, "0")
    self.chain.append(genesis_block)
    return self.chain

  # prints contents of blockchain
  def print_blocks(self):
    for i in range(len(self.chain)):
      current_block = self.chain[i]
      print("Block {} {}".format(i, current_block))
      current_block.print_contents()    
  
  # add block to blockchain `chain`
  def add_block(self, vote_data):
    previous_block_hash = self.chain[len(self.chain)-1].hash
    new_block = Block(vote_data, previous_block_hash)
    proof = self.proof_of_work(new_block)
    #new_block.hash = proof
    # modify this method
    self.chain.append(new_block)
    return proof, new_block
    

  def validate_chain(self):
    print("Validating Chain.")
    for i in range(1, len(self.chain)):
      current = self.chain[i]
      previous = self.chain[i-1]
      #print("current.previous_hash, previous.hash: ",current.previous_hash," ",previous.hash)
      #print("validating block chain: ",self.chain)
      #print("current hash vs current.generate_hash vs current.vote_data: ",current.hash," ",current.generate_hash()," ",current.vote_data)
      if(current.hash != current.generate_hash()):
        print("The current hash of the block does not equal the generated hash of the block.")
        return False
      if(current.previous_hash != previous.generate_hash()):
        print("The previous block's hash does not equal the previous hash value stored in the current block.")
        return False
      if current.hash[:self.difficulty] != '0'*self.difficulty:
        print("Proof of work is not valid enough.")
        return False
    return True
  
  #Increase difficulty to increase the time it takes to validate a block and the security of the block
  def proof_of_work(self,block):
    #print("Generating proof of work.")
    self.done_signal=0
    proof = block.generate_hash()
    block.nonce=random.randint(0, 900000000000000000)
    while proof[:self.difficulty] != '0'*self.difficulty:
      block.nonce += 1
      proof = block.generate_hash()
      block.hash = proof
      if self.done_signal:
        #print("\n\n\nDone Signal Triggered. Exiting Early\n\n\n")
        return 0
    #block.nonce = 0
    return proof




