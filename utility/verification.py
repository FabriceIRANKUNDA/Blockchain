"""Provides verification helper methods."""
from utility.hash_util import hash_string_256, hash_block
from wallet import Wallet

class Verification:
    @staticmethod
    def valid_proof(transactions, last_hash, proof_number):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof_number)).encode()
        hash_guess = hash_string_256(guess)

        return hash_guess[0:2] == "00" 
    @classmethod
    def verify_blockchain(cls, block_chain):
        if len(block_chain) == 1:
            return True
        for index, block in enumerate(block_chain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(block_chain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid")
                return False
        return True

    @staticmethod    
    def verify_transaction(transaction, get_balance, check_funds=True):
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            is_sufficient_balance = sender_balance > transaction.amount
            is_auth = Wallet.verify_transaction(transaction)
            
            return is_sufficient_balance and is_auth
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions]) 