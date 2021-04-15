import hashlib
import json

def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
     # Hash the previous block using SHA256 by first convert it to a string using json library
     #And finally convert the returned bytes value to a string using hexdigest method
    return hash_string_256(json.dumps(block, sort_keys=True).encode())