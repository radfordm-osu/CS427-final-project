from hashlib import sha256
import bcrypt
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Util.Padding import pad

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
    h.update(key.encode("utf-8"))
    key = h.digest()
    #print(len(key))
    #print(key)

    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
    iv = cipher.iv

    #iv = Random.new().read(AES.block_size)
    #cipher = AES.new(key, AES.MODE_CBC, iv)

    return str(ct)

def decrypt(key, data, iv):

    h = SHA256.new()
    h.update(key.encode("utf-8"))
    key = h.digest()

    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    pt = unpad(cipher.decrypt(data), AES.block_size)

    return pt
