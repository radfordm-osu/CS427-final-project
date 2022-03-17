from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from base64 import b64encode
from base64 import b64decode
import argon2

#Argon2 Hash of data
def H(data):
	#Uses settings defined in security write up and from Argon2 report
	#Time cost of 6 iterative passes over memory
	#Memory cost of 2 GBs
	#Parallelism of 8 threads
	#Hash length of 256 bits
	#Salt length of 128 bits
	ph = argon2.PasswordHasher(time_cost=6, memory_cost=2097152, parallelism=4, hash_len=32, salt_len=16)
	final = ph.hash(data)
	return final

#Checks the hash against user inputted master password
def checkPass(password, data):
	ph = argon2.PasswordHasher(time_cost=6, memory_cost=2097152, parallelism=4, hash_len=32, salt_len=16)
	if ph.verify(data, password):
		#If the stored hash is the same as the master password
		return 1
	else:
		#If the stored hash is different than the inputted master password
		return -1

#Runs the AES key encryption on the master password
def H2(data):
	#Uses same settings as before, but static salt so that the key stays consistent between runs
	final = argon2.hash_password_raw(time_cost=6, memory_cost=2097152, parallelism=4, hash_len=32, password=data, salt=b'saltysaltsalter')
	return final

def write_iv(iv, uname):
    idx = 0
    line_no = 0
    # Get the data
    with open("users/users.txt", "r") as file:
        data = file.readlines()
    # Get the line number of the iv
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
    key1 = H2(key.encode("utf-8"))
    #Generates a cipher with a hash of master password as the key
    cipher = AES.new(key1, AES.MODE_CBC)
    #Encrypts the data with the generated AES cipher
    ct = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
    ct_use = b64encode(ct).decode("utf-8")
    iv = cipher.iv
    #Writes the ciphertext to the user's file
    write_iv(iv, uname)
    return ct_use

def decrypt(key, data, uname):
    #Regenerates the key from the user's master password
    key1 = H2(key.encode("utf-8"))
    iv = get_iv(uname)
    #Uses the key and generates a cipher to decrypt
    cipher = AES.new(key1, AES.MODE_CBC, iv)
    d2 = b64decode(data)
    #Decrypts the ciphertext and returns the plaintext
    pt = unpad(cipher.decrypt(d2), AES.block_size)
    return pt.decode("utf-8")
