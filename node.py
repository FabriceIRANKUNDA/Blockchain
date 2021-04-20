from uuid import uuid4


from blockchain import Blockchain
from utility.verification import Verification

class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = "Fabu"
        self.blockchain = Blockchain(self.id)

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
            print("Q ----> Quit")

            user_choice = self.get_user_choice()

            if user_choice == "1":
                recipient, amount = self.get_transaction_value()
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print("Transaction added successfuly!")
                else:
                    print("Transactin failed!")
                print(self.blockchain.get_open_transactions())
            elif user_choice == "2":
                self.blockchain.mine_block()

            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transanction")
            elif user_choice.lower() == 'q':
                break
            else:
                print("Invalid input, Please enter an option from those displayed on your screen!")
            if not Verification.verify_blockchain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("Invalid blockchain!")
                break
            print("Balance of {}: {:6.2f}".format(self.id, self.blockchain.get_balance()))
        print("Done!")

if __name__ == "__main__":
    node = Node()
    node.listen_to_user_input()