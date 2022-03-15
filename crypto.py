from hashlib import sha256
import bcrypt
import argon2

def H(data):
    # Method 1
#    hash = sha256()
#    hash.update(data)
#    final = hash.hexdigest()
    #salt = bcrypt.gensalt()
    #final = bcrypt.hashpw(data.encode('utf-8'), salt)
	ph = argon2.PasswordHasher(time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)
	final = ph.hash(data)
	return final

def checkPass(password, data):
    # Hash the password against the hash
    #if bcrypt.checkpw(password.encode('utf-8'), data.encode('utf-8')):
	if argon2.PasswordHasher.verify(data, password):
		return 1
	else:
		return -1

def encrypt(key, data):
    return data+key

def decrypt(key, data):
    return data.replace(key, '')
