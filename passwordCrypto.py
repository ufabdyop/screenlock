import hashlib

def encrypt(password):
    return hashlib.sha224(password).hexdigest()
