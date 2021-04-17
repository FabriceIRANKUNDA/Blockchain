import functools
import json
import hashlib
import pickle
from collections import OrderedDict

from hash_util import hash_string_256, hash_block


MINING_REWARD = 10
owner = "Fabu"
participants ={"Fabu"}


def load_data():
    try:
        with open("blockchain.txt", mode="r") as f:
            file_content = f.readlines()
            # file_content = pickle.loads(f.read())
            if len(file_content) > 0:
                global block_chain
                global open_transactions
                # block_chain = file_content["chain"]
                # open_transactions = file_content["ot"]
                block_chain = json.loads(file_content[0][:-1])
                block_chain = [ {"previous_hash": block["previous_hash"], "index": block["index"], "proof": block["proof"], "transactions": [ OrderedDict([("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])]) for tx in block["transactions"]]} for block in block_chain]
                open_transactions = json.loads(file_content[1])
                open_transactions = [OrderedDict([("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])]) for tx in open_transactions]
    except EOFError:
        genesis_block = {
        "previous_hash": "",
        "index": 0,
        "transactions": [],
        "proof": 100
        }
        block_chain = [genesis_block]
        open_transactions = []

load_data()


def save_data():
    try:
        with open("blockchain.txt", mode="w") as f:
            """
                Both json and pickle can help us but pickle is more flexible because it does change the structure of our OdererdDict
                Pickle also write our data as bytes not text
            """
            f.write(json.dumps(block_chain))
            f.write("\n")
            f.write(json.dumps(open_transactions))
            # saved_data = {
            #     "chain": block_chain,
            #     "ot": open_transactions
            # }
            # f.write(pickle.dumps(saved_data))
    except:
        print("Saving failed")


def valid_proof(transactions, last_hash, proof_number):
    guess = (str(transactions) + str(last_hash) + str(proof_number)).encode()
    hash_guess = hash_string_256(guess)

    return hash_guess[0:2] == "00"


def proof_of_work():
    last_block = block_chain[-1]
    last_hash = hash_block(last_block)
    proof_number = 0

    while not valid_proof(open_transactions, last_hash, proof_number):
        proof_number += 1
    return proof_number


def get_balance(participant):
    tx_sender = [ [ tx["amount"] for tx in block["transactions"] if tx["sender"] == participant] for block in block_chain]
    open_txt_sender =  [txt["amount"] for txt in open_transactions if txt["sender"] == participant]
    tx_sender.append(open_txt_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_sender, 0)
    
    tx_recipient = [ [ tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant] for block in block_chain]
    amount_recieved = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_recipient, 0)
    
    return amount_recieved - amount_sent
def get_last_blockchain_value():
    if len(block_chain) < 1:
        return None
    return block_chain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance > transaction["amount"]
    
 
def add_transaction(recipient, sender=owner, amount=1.0):
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

    transaction = OrderedDict([("sender", sender), ("recipient", recipient), ("amount", amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False
 

def get_transaction_value():
    txt_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Please enter your transaction amount: "))
    return txt_recipient, tx_amount


def mine_block():
    last_block = block_chain[-1]
    hashed_block =  hash_block(last_block)
    proof = proof_of_work()
    # reward_transaction = {
    #     "sender":"MINING",
    #     "recipient": owner,
    #     "amount": MINING_REWARD
    # }
    reward_transaction = OrderedDict([("sender", "MINING"), ("recipient", owner), ("amount", MINING_REWARD)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        "previous_hash": hashed_block,
        "index": len(block_chain),
        "transactions": copied_transactions,
        "proof": proof
    }
    block_chain.append(block)
    return True


def get_user_choice():
    user_input = input("Enter your choice: ")
    return user_input 


def print_blockchain_elements():
    for block in block_chain:
        print("Outputting Block: ", block)


def verify_blockchain():
    if len(block_chain) == 1:
        return True
    for index, block in enumerate(block_chain):
        if index == 0:
            continue
        if block["previous_hash"] != hash_block(block_chain[index - 1]):
            return False
        if not valid_proof(block["transactions"][:-1], block["previous_hash"], block["proof"]):
            print("Proof of work is invalid")
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])

def list_comprehension(*numbers):
    new_list = [number * 2 for number in numbers]
    return new_list

while True:
    print("Make a choice")
    print("1: Add new transaction value")
    print("2: Mine a new block")
    print("3: Outputting the blockchain blocks")
    print("4: Output participants")
    print("5: Check transactions validity")
    print("h: Manipulate the chain")
    print("Q ----> Quit")

    user_choice = get_user_choice()

    if user_choice == "1":
        recipient, amount = get_transaction_value()
        if add_transaction(recipient,amount=amount):
            print("Transaction added successfuly!")
        else:
            print("Transactin failed!")
        print(open_transactions)
    elif user_choice == "2":
       if mine_block():
           open_transactions = []
           save_data()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print(f"Participants: {participants}")
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transanction")
    elif user_choice.lower() == 'h':
        if len(block_chain) >= 1:
            block_chain[0] = {
                "previous_hash": "",
                "index": 0,
                "transactions": [{"sender": "Papy", "recipient": "Max", "amount": 100.0}]
            }
    elif user_choice.lower() == 'q':
        break
    else:
        print("Invalid input, Please enter an option from those displayed on your screen!")
    if not verify_blockchain():
        print("Invalid blockchain!")
        break
    print("Balance of {}: {:6.2f}".format("Fabrice", get_balance("Fabu")))
        

print("Done!")