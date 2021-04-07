block_chain = []
open_transaction = []

def get_last_blockchain_value():
    if len(block_chain) < 1:
        return None
    return block_chain[-1]
 
def add_transaction(transaction_amount, last_transaction_value= [1]):
    last_transaction_value = [1] if last_transaction_value == None else last_transaction_value
    block_chain.append([last_transaction_value, transaction_amount])



def get_transaction_value():
    return float(input("Please enter your transaction amount: "))

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
    print("2: Outputting the blockchain blocks")
    print("h: Manipulate the chain")
    print("Q ----> Quit")

    user_choice = get_user_choice()

    if user_choice == "1":
        tx_amount= get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == "2":
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


