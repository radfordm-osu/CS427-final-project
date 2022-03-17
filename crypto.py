from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from base64 import b64encode
from base64 import b64decode
import argon2

def H(data):
	ph = argon2.PasswordHasher(time_cost=6, memory_cost=2097152, parallelism=4, hash_len=32, salt_len=16)
	final = ph.hash(data)
	return final

def checkPass(password, data):
    # Hash the password against the hash
	ph = argon2.PasswordHasher(time_cost=6, memory_cost=2097152, parallelism=4, hash_len=32, salt_len=16)
	if ph.verify(data, password):
		return 1
	else:
		return -1

def write_iv(key, data):
    # Get the line number of the
    with open("users/users.txt", "r") as file:
        for line in file:
            idx += 1
            # If the username is a match, set the flag
            if uname == line.strip():
                line_no = idx

    # Replace the line storing the IV
    data[line_no] = b64encode(iv).decode('utf-8')
    with open("users/users.txt", "w") as file:
        for i in range(0, len(data)):
            file.write(data[i].strip()+"\n")

def get_iv(uname):
    idx = 0
    line_no = 0
    # Get the data
    with open("users/users.txt", "r") as file:
        data = file.readlines()
    # Find the username line
    with open("users/users.txt", "r") as file:
        for line in file:
            idx += 1
            # If the username is a match, set the flag
            if uname == line.strip():
                line_no = idx
    # retrieve the IV
    iv = b64decode(data[line_no].strip())
    return iv

def encrypt(key, data, uname):
    #h = SHA256.new()
    #h.update(key.encode("utf-8"))
    #key = h.digest()
    #print(len(key))
    #print(key)

    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC)
    ct = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
    ct_use = b64encode(ct).decode("utf-8")
    iv = cipher.iv
    print(ct)
    write_iv(iv, uname)

    #iv = Random.new().read(AES.block_size)
    #cipher = AES.new(key, AES.MODE_CBC, iv)

    return ct_use

def decrypt(key, data, uname):

    #h = SHA256.new()
    #h.update(key.encode("utf-8"))
    #key = h.digest()

    iv = get_iv(uname)
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)
    d2 = b64decode(data)
    pt = unpad(cipher.decrypt(d2), AES.block_size)
    return pt.decode("utf-8")

