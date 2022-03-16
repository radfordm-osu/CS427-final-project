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
    #salt = bcrypt.gensalt()
    #final = bcrypt.hashpw(data.encode('utf-8'), salt)
    return data, data

def checkPass(password, data):
    # Hash the password against the hash
    #if bcrypt.checkpw(password.encode('utf-8'), data.encode('utf-8'))
    return 1
   # else:
   #     return -1

def write_iv(iv, uname):
    idx = 0
    line_no = 0
    with open("users/users.txt", "r") as file:
        data = file.readlines()

    # Get the line number of the
    with open("users/users.txt", "r") as file:
        for line in file:
            idx += 1
            # If the username is a match, set the flag
            if uname == line.strip():
                line_no = idx + 1

    # Replace the line storing the IV
    data[line_no] = iv.decode("utf-8")
    with open("users/users.txt", "w") as file:
        for i in range(0, len(data)):
            file.write(str(data[i]))

        #file.writelines(str(data))

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
                line_no = idx + 1

    # retrieve the IV
    iv = data[line_no].encode("utf-8")
    return iv

def encrypt(key, data, uname):
    #h = SHA256.new()
    #h.update(key.encode("utf-8"))
    #key = h.digest()
    #print(len(key))
    #print(key)

    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC)
    ct = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
    iv = cipher.iv
    write_iv(iv, uname)

    #iv = Random.new().read(AES.block_size)
    #cipher = AES.new(key, AES.MODE_CBC, iv)

    return str(ct)

def decrypt(key, data, uname):

    #h = SHA256.new()
    #h.update(key.encode("utf-8"))
    #key = h.digest()


    iv = get_iv(uname)

    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    pt = unpad(cipher.decrypt(data), AES.block_size)

    return pt
