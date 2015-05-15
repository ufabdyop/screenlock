import hashlib

SCREENLOCKSALT="RLZI8y0U6nbhwYLAItcZezaMIQIzQupVITAMfwE25"

def encrypt(password):
    return hashlib.sha224(SCREENLOCKSALT + password).hexdigest()
