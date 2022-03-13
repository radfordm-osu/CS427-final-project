from hashlib import sha256
import bcrypt
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def H(data):
    # Method 1
#    hash = sha256()
#    hash.update(data)
#    final = hash.hexdigest()
    salt = bcrypt.gensalt()
    final = bcrypt.hashpw(data.encode('utf-8'), salt)
    return final, salt

def checkPass(password, data):
    # Hash the password against the hash
    if bcrypt.checkpw(password.encode('utf-8'), data.encode('utf-8')):
        return 1
    else:
        return -1

def encrypt(key, data):
    h = SHA256.new()
    h.update(key)
    key = h.digest()

    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return cipher.encrypt(data), key

def decrypt(key, data):
    plain = AES.new(key, AES.MODE_CBC, iv)

    return plain.decrypt(data)
