from uuid import uuid4


from blockchain import Blockchain
from wallet import Wallet
from utility.verification import Verification

class Node:
    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys() 
        self.blockchain = Blockchain(self.wallet.public_key) 
    def get_transaction_value(self):
        txt_recipient = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Please enter your transaction amount: "))
        return txt_recipient, tx_amount

    def get_user_choice(self):
        user_input = input("Enter your choice: ")
        return user_input 

    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print("Outputting Block: ", block)

    def listen_to_user_input(self):
        waiting_for_user_input = True
        while waiting_for_user_input:
            print("Make a choice")
            print("1: Add new transaction value")
            print("2: Mine a new block")
            print("3: Outputting the blockchain blocks")
            print("4: Check transactions validity")
            print("5: Create wallet")
            print("6: Load wallet")
            print("7: Save keys")
            print("Q ----> Quit")

            user_choice = self.get_user_choice()

            if user_choice == "1":
                recipient, amount = self.get_transaction_value()
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print("Transaction added successfuly!")
                else:
                    print("Transaction failed!")
                print(self.blockchain.get_open_transactions())
            elif user_choice == "2":
                if not self.blockchain.mine_block():
                    print("Mining failed. Got no wallet?")

            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transanction")
            elif user_choice == "5":
                  self.wallet.create_keys() 
                  self.blockchain = Blockchain(self.wallet.public_key) 
            elif user_choice == "6":
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "7":
                self.wallet.save_keys()
            elif user_choice.lower() == 'q':
                break
            else:
                print("Invalid input, Please enter an option from those displayed on your screen!")
            if not Verification.verify_blockchain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("Invalid blockchain!")
                break
            print("Balance of {}: {:6.2f}".format(self.wallet.public_key, self.blockchain.get_balance()))
        print("Done!")

if __name__ == "__main__":
    node = Node()
    node.listen_to_user_input()