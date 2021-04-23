import functools
import json
import hashlib
import pickle

from utility.hash_util import hash_block
from block import Block
from transaction import Transaction
from utility.verification import Verification
from wallet import Wallet

MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, "", [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.hosting_node = hosting_node_id
        self.__peer_nodes = set()
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]
    
    @chain.setter
    def chain(self, val):
        self.__chain = val
    
    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open("blockchain.txt", mode="r") as f:
                file_content = f.readlines()
                # file_content = pickle.loads(f.read())
                if len(file_content) > 0:
                    # global block_chain
                    # global open_transactions
                    # block_chain = file_content["chain"]
                    # open_transactions = file_content["ot"]
                    self.chain = json.loads(file_content[0][:-1])
                    # block_chain = [Block(block["index"], block["previous_hash"], [ OrderedDict([("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])]) for tx in block["transactions"]], block["proof"], block["timestamp"]) for block in block_chain]
                    self.chain = [ Block(block["index"], block["previous_hash"], [ Transaction(tx["sender"], tx["recipient"], tx["signature"], tx["amount"]) for tx in block["transactions"]], block["proof"], block["timestamp"]) for block in self.__chain ] 
                    # block_chain = [ {"previous_hash": block["previous_hash"], "index": block["index"], "proof": block["proof"], "transactions": [ OrderedDict([("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])]) for tx in block["transactions"]]} for block in block_chain]
                    self.__open_transactions = json.loads(file_content[1][:-1])
                    self.__open_transactions = [Transaction(tx["sender"], tx["recipient"], tx["signature"], tx["amount"]) for tx in self.__open_transactions]
                    # open_transactions = [OrderedDict([("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])]) for tx in open_transactions]
                    peer_nodes = json.loads(file_content[2])
                    self.__peer_nodes = set(peer_nodes)
        except (FileNotFoundError, IndexError):
            print("Handled Exception..")

    def save_data(self):
        try:
            with open("blockchain.txt", mode="w") as f:
                """
                    Both json and pickle can help us but pickle is more flexible because it does change the structure of our OdererdDict
                    Pickle also write our data as bytes not text
                """
                savable_chain = [ block.__dict__ for block in [ Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain ]]
                f.write(json.dumps(savable_chain))
                f.write("\n")
                savable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(savable_tx))
                f.write("\n")
                f.write(json.dumps(list(self.__peer_nodes)))
                # saved_data = {
                #     "chain": block_chain,
                #     "ot": open_transactions
                # }
                # f.write(pickle.dumps(saved_data))
        except:
            print("Saving failed")


    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof_number = 0

        while not Verification.valid_proof(self.__open_transactions, last_hash, proof_number):
            proof_number += 1
        return proof_number

    def get_balance(self):
        if self.hosting_node == None:
            return None
        participant = self.hosting_node
        tx_sender = [ [ tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_txt_sender =  [txt.amount for txt in self.__open_transactions if txt.sender == participant]
        tx_sender.append(open_txt_sender)
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_sender, 0)
        
        tx_recipient = [ [ tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_recieved = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_recipient, 0)
        
        return amount_recieved - amount_sent

    def get_last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]
    
    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new tranction

        Arguments:
            : sender: The sender of the coins
            : recipient: The recipient of the coins
            : amount: The amount of coins sent with the transaction (default = 1.0)
            : Use OrderedDict to control the order of our dictionary to avoid invalid hash coincidence
        """
        # transaction = {
        #     "sender": sender,
        #     "recipient": recipient,
        #     "amount": amount
        # }

        if self.hosting_node == None:
            return False

        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        if self.hosting_node == None:
            return None
        last_block = self.__chain[-1]
        hashed_block =  hash_block(last_block)
        proof = self.proof_of_work()
        # reward_transaction = {
        #     "sender":"MINING",
        #     "recipient": owner,
        #     "amount": MINING_REWARD
        # }
        reward_transaction = Transaction( "MINING", self.hosting_node, "", MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
    
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block
    
    def add_peer_node(self, node):
        """Adds a new node to the peer node set

        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()
    
    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        return list(self.__peer_nodes)