import hashlib
import json

__all__ = ["hash_string_256", "hash_block"]

def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
     # Hash the previous block using SHA256 by first convert it to a string using json library
     #And finally convert the returned bytes value to a string using hexdigest method
    hashable_block = block.__dict__.copy()
    hashable_block["transactions"] = [tx.to_ordered_dict() for tx in hashable_block["transactions"]]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())