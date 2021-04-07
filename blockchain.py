genesis_block = {
    "previous_hash": "",
     "index": 0,
     "transactions": []
}
block_chain = [genesis_block]
open_transaction = []
owner = "Fabu"

def get_last_blockchain_value():
    if len(block_chain) < 1:
        return None
    return block_chain[-1]
 
def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new tranction

    Arguments:
        : sender: The sender of the coins
        : recipient: The recipient of the coins
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }
    open_transaction.append(transaction)

  

def get_transaction_value():
    txt_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Please enter your transaction amount: "))
    return txt_recipient, tx_amount


def mine_block():
    last_block = block_chain[-1]
    hash = ""

    for key in last_block:
        value = last_block[key]
        hash_block +=  value + '_' 
    
    block = {
        "previous_hash": hash_block, 
        "index": len(block_chain),
        "transactions": open_transaction
    }
    block_chain.append(block)


def get_user_choice():
    user_input = input("Enter your choice: ")
    return user_input 


def print_blockchain_elements():
    for block in block_chain:
            print("Outputting Block: ", block)


def verify_blockchain():
    block_index = 0
    is_valid = True

    for block in block_chain:
        if type(block[0]) != list:
            is_valid = False
            break
        elif block_index == 0:
            block_index += 1
            continue
        elif block[0] == block_chain[block_index - 1]:
            is_valid = True
            block_index += 1
        else:
            is_valid = False
            break
    return is_valid


while True:
    print("Make a choice")
    print("1: Add new transacrion value")
    print("2: Mine a new block")
    print("3: Outputting the blockchain blocks")
    print("h: Manipulate the chain")
    print("Q ----> Quit")

    user_choice = get_user_choice()

    if user_choice == "1":
        recipient, amount = get_transaction_value()
        add_transaction(recipient,amount=amount)
        print(open_transaction)
    elif user_choice == "2":
        mine_block()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice.lower() == 'h':
        if len(block_chain) >= 1:
            block_chain[0] = [2]
    elif user_choice.lower() == 'q':
        break
    else:
        print("Invalid input, Please enter an option from those displayed on your screen!")
    if not verify_blockchain():
        print("Invalid blockchain!")
        break
        

print("Done!") 


