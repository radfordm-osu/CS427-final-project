from hashlib import sha256
import bcrypt

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
    return data+key

def decrypt(key, data):
    return data.replace(key, '')
