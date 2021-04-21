from flask import Flask, jsonify
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)

"""
    Create our server listening on port 5000
    Add route to respond to any get request with a path
    Add a function to handle request targeting the specified route
"""
@app.route("/", methods=["GET"])
def get_ui():
    return "This works!"

@app.route("/wallet", methods=["POST"])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        response ={
            "public key": wallet.public_key,
            "private key": wallet.private_key
        }
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        return jsonify(response), 201
    else:
        response = {
            "message": "Saving keys failed."
        }
        return jsonify(response), 500

@app.route("/wallet", methods=["GET"])
def load_keys():
    if wallet.load_keys():
        response ={
            "public key": wallet.public_key,
            "private key": wallet.private_key
        }
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        return jsonify(response), 201
    else:
        response = {
            "message": "Loading keys failed."
        }
        return jsonify(response), 500


@app.route("/mine", methods=["POST"])
def mine():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]
        response = {
            "message": "Block added successfuly.",
            "block": dict_block
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Adding a block failed",
            "wallet_set_up": wallet.public_key != None
        }
        return jsonify(response), 400

"""
    This will return the chain pre-initiated by the blockchain constructor
    and return it as response the to request.
    Typecast all block and transaction objects to dictionary for json serializable
"""    

@app.route("/chain", methods=["GET"])
def get_chain():
    chain_snapshot = blockchain.chain 
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]
    return jsonify(dict_chain), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)