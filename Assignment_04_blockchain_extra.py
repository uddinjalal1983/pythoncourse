import datetime as dt
import hashlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import unittest
import uuid


class PandasChain:
    # 5 pts - Complete this constructor
    def __init__(self, name): 
        self.__name = name # Convert name to upper case and store it here
        self.__chain = [] # Create an empty list
        self.__id = hashlib.sha256(str(str(uuid.uuid4())+self.__name+str(dt.datetime.now())).encode('utf-8')).hexdigest()
        # Create a sequence ID and set to zero
        self.__prev_hash = None # Set to None
        self.__seq_id = 0
        self.__current_block = Block(self.__seq_id,self.__prev_hash) # Create a new Block 
        self.__chain.append(self.__current_block)
        print(self.__name,'PandasChain created with ID',self.__id,'chain started.')
    
    # 5 pts - This method should loop through all committed and uncommitted blocks and display all transactions in them
    def display_chain(self): 
        for block in self.__chain:
        	block.display_transactions()
    
    # This method accepts a new transaction and adds it to current block if block is not full. 
    # If block is full, it will delegate the committing and creation of a new current block 
    def add_transaction(self,s,r,v): 
        if self.__current_block.get_size() >= 10:
            self.__commit_block(self.__current_block)
        self.__current_block.add_transaction(s,r,v)
    
    # 10 pts - This method is called by add_transaction if a block is full (i.e 10 or more transactions). 
    # It is private and therefore not public accessible. It will change the block status to committed, obtain the merkle
    # root hash, generate and set the block's hash, set the prev_hash to the previous block's hash, append this block 
    # to the chain list, increment the seq_id and create a new block as the current block
    def __commit_block(self,block): 
        # Add code here
        self.__current_block.set_status("COMMITTED")
        # Create block hash
        self.__prev_hash = hashlib.sha256(str(self.__prev_hash)+str(self.__id)+str(dt.datetime.now()).encode('utf-8')+str(self.__seq_id)+str(self.__current_block.get_simple_merkle_root())).hexdigest()
        self.__current_block.set_block_hash(self.__prev_hash)
        self.__seq_id += 1
        self.__chain.append(Block(self.__seq_id,self.__prev_hash))
        self.__current_block = self.__chain[self.__seq_id]
        # self.__prev_hash = self.__current_block.
        # Add code here
        print('Block committed')
    
    # 10 pts - Display just the metadata of all blocks (committed or uncommitted), one block per line.  
    # You'll display the sequence Id, status, block hash, previous block's hash, merkle hash and total number (count) 
    # of transactions in the block
    def display_block_headers(self): 
        for block in self.__chain:
        	block.display_header()
    
    # 5 pts - return int total number of blocks in this chain (committed and uncommitted blocks combined)
    def get_number_of_blocks(self): 
        return len(self.__chain)
    
    # 10 pts - Returns all of the values (Pandas coins transferred) of all transactions from every block as a single list
    def get_values(self):
        coins = [] 
        ts = []
        for block in self.__chain:
        	t,c = block.get_values()
        	ts += t
        	coins += c
        return np.array(ts),np.array(coins)

            
class Block:
    # 5 pts for constructor
    def __init__(self,seq_id,prev_hash): 
        self.__seq_id = seq_id # Set to what's passed in from constructor
        self.__prev_hash = prev_hash # From constructor
        self.__col_names = ['Timestamp','Sender','Receiver','Value','TxHash']
        self.__transactions = pd.DataFrame(columns = self.__col_names) # Create a new blank DataFrame with set headers
        self.__status = "UNCOMMITED" # Initial status. This will be a string.
        self.__block_hash = None
        self.__merkle_tx_hash = None
        
    #5 pts -  Display on a single line the metadata of this block. You'll display the sequence Id, status, 
    # block hash, previous block's hash, merkle hash and number of transactions in the block
    def display_header(self): 
        print (self.__seq_id,self.__status,self.__block_hash,self.__prev_hash,self.__merkle_tx_hash,self.get_size())
    
    # 10 pts - This is the interface for how transactions are added
    def add_transaction(self,s,r,v): 
    	import time
        ts = time.time() # Get current timestamp 
        tx_hash = hashlib.sha256(str(ts)+s+r+str(v)).hexdigest() # Hash of timestamp, sender, receiver, value
        new_transaction = pd.DataFrame([[ts,s,r,v,tx_hash]],columns = self.__col_names) # Create DataFrame with transaction data (a DataFrame with only 1 row)
        # Append to the transactions data
        self.__transactions = self.__transactions.append(new_transaction)
        
    # 10 pts -Print all transactions contained by this block
    def display_transactions(self): 
    	for index, row in self.__transactions.iterrows():
    		print(row['Timestamp'], row['Sender'],row['Receiver'],str(row['Value']),row['TxHash'])
    
    # 5 pts- Return the number of transactions contained by this block
    def get_size(self): 
        return self.__transactions.shape[0]
    
    # 5 pts - Setter for status - Allow for the change of status (only two statuses exist - COMMITTED or UNCOMMITTED). 
    # There is no need to validate status.
    def set_status(self,status):
        self.__status = status
    
    # 5 pts - Setter for block hash
    def set_block_hash(self,hash):
        self.__block_hash = hash
    
    # 10 pts - Return and calculate merkle hash by taking all transaction hashes, concatenate them into one string and
    # hash that string producing a "merkle root" - Note, this is not how merkle tries work but is instructive 
    # and indicative in terms of the intent and purpose of merkle tries
    def get_simple_merkle_root(self):
    	txHash = '' 
        for index, row in self.__transactions.iterrows():
        	txHash += row['TxHash']
        self.__merkle_tx_hash = hashlib.sha256(txHash).hexdigest()
        return self.__merkle_tx_hash
    
    def get_values(self):
        values = []
        ts = []
        for index, row in self.__transactions.iterrows():
        	values.append(row['Value'])
        	ts.append(row['Timestamp'])
        return  ts,values


class TestAssignment4(unittest.TestCase):
    def test_chain(self):
        block = Block(1,"test")
        self.assertEqual(block.get_size(),0)
        block.add_transaction("Bob","Alice",50)
        self.assertEqual(block.get_size(),1)
        pandas_chain = PandasChain('testnet')
        self.assertEqual(pandas_chain.get_number_of_blocks(),1)
        pandas_chain.add_transaction("Bob","Alice",50)
        pandas_chain.add_transaction("Bob","Alice",51)
        pandas_chain.add_transaction("Bob","Alice",52)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        self.assertEqual(pandas_chain.get_number_of_blocks(),2)
        pandas_chain.add_transaction("Bob","Alice",50)
        pandas_chain.add_transaction("Bob","Alice",51)
        pandas_chain.add_transaction("Bob","Alice",52)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        # pandas_chain.display_block_headers()
        # pandas_chain.display_chain()
        self.assertEqual(pandas_chain.get_number_of_blocks(),3)
        x,y = pandas_chain.get_values()
        plt.plot(x,y)
        plt.show()


if __name__ == '__main__':
    unittest.main()
