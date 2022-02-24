import crypto
from hashlib import sha256
from colorama import init, Fore
import string
import random
import os


# Get existing usernames
def getUsers():
    users = []
    with open("users/users.txt", "r") as file:
        idx = 2;
        for line in file:
            idx += 1
            if idx % 3 == 0:
                users.append(line.strip())
    # return what was found
    return users


# Sign up for the service
def signup():
    print(Fore.CYAN + "\n\n#=#=#=#=#=#=#=#=#=#=#=#=#")
    print(Fore.GREEN + "- Sign Up for PassVault -")
    print(Fore.CYAN + "#=#=#=#=#=#=#=#=#=#=#=#=#\n")

    # Ask for a username
    print(" Enter a username, or 'q' to cancel signup")
    print(Fore.YELLOW + " NOTE: usernames must be between 6 and 14 characters\n")
    uname = input("@pv> ")

    # if the user chose to quit
    if uname == "q" or uname == "Q": return 1

    # Tell the user what went wrong and re-take input
    while(good_uname(uname) < 0 and uname != "q" and uname != "Q"):
        if good_uname(uname) == -1: print(Fore.RED + "\n That username is too short!")
        elif good_uname(uname) == -2: print(Fore.RED + "\n That username is too long!")
        elif good_uname(uname) == -3: print(Fore.RED + "\n That username is in use!")
        elif good_uname(uname) == -4: print(Fore.RED + "\n That username contains whitespace!")
        print(" Enter a username, or 'q' to cancel signup")
        print(Fore.YELLOW + " NOTE: usernames must be between 6 and 14 characters\n")
        uname = input("@pv> ")

    # if the user chose to quit
    if uname == "q" or uname == "Q": return 1

    pw = set_password()

    if pw == -1: return 1

    # Register the user then return
    register(uname, pw)


# Have the user set a password, then save it
def set_password():
    # Ask the user to generate a password
    print("\n\n Enter a password, or 'q' to cancel signup")
    print(" Alternatively, enter 'auto' to have a password generated for you.\n")
    print(Fore.YELLOW + " NOTES:")
    print(Fore.YELLOW + "  Passwords must be between 6 and 20 characters and contain at least 1 special character,")
    print(Fore.YELLOW + "  1 number, 1 uppercase character and 1 lowercase character\n")
    pw = input("@pv> ")

    # if the user chose to quit
    if pw == "q" or pw == "Q": return 1

    # Generate a password
    if pw == "auto":
        pw = passGen(16)
        print(Fore.RED + "\n\n!!! BE SURE TO WRITE THIS DOWN SOMEWHERE SAFE !!!")
        print(" Your password is:")
        print(Fore.GREEN + pw)

    # Otherwise, check the password
    else:
        while (good_password(pw) < 0 and pw != "q" and pw != "Q"):
            if good_password(pw) == -1: print(Fore.RED + "\n Password is too short!")
            elif good_password(pw) == -2: print(Fore.RED + "\n Password is too long!")
            elif good_password(pw) == -3: print(Fore.RED + "\n Password does not meet the minimum requirements!")
            elif good_password(pw) == -4: print(Fore.RED + "\n Password contains whitespace!")

            # Ask the user to generate a password
            print(" Enter a password, or 'q' to cancel signup")
            print(" Alternatively, enter 'auto' to have a password generated for you.\n")
            print(Fore.YELLOW + " NOTES:")
            print(Fore.YELLOW + "  Passwords must be between 6 and 20 characters and contain at least 1 special character,")
            print(Fore.YELLOW + "  1 number, 1 uppercase character and 1 lowercase character\n")
            pw = input("@pv> ")
        # if the user chose to quit
        if pw == "q" or pw == "Q": return -1
    return pw

# create a new user entry
def register(name, password):
    # open the file in appending mode
    ufile = open("users/users.txt", "a")
    # hash the password for storage
    (pw, salt) = crypto.H(password)
    ufile.write(name)
    ufile.write("\n")
    ufile.write(salt.decode("utf-8"))
    ufile.write("\n")
    ufile.write(pw.decode("utf-8"))
    ufile.write("\n")
    ufile.close()
    return 1


# Check if the password follows best practices
def good_password(pw):
    # Check the length
    if len(pw) < 6:
        return -1
    elif len(pw) > 20:
        return -2

    # check the minimum requirements
    digit_flag = 0
    upper_flag = 0
    lower_flag = 0
    other_flag = 0
    whitespace_flag = 0
    for char in pw:
        # check for digits
        if char in string.digits:
            digit_flag = 1
        # check for uppercase letters
        elif char in string.ascii_uppercase:
            upper_flag = 1
        # check for lowercase letters
        elif char in string.ascii_lowercase:
            lower_flag = 1
        # check for other chars
        elif char in string.punctuation:
            other_flag = 1
        elif char in string.whitespace:
            whitespace_flag = 1

    # if the flags are not all set (except whitespace), return an error
    if digit_flag == 0 or upper_flag == 0 or lower_flag == 0 or other_flag == 0: return -3
    elif whitespace_flag: return -4
    else: return 1

# Check a username
def good_uname(uname):
    # if the username is too short or too long, return an error code
    if len(uname) < 3: return -1
    elif len(uname) > 14: return -2

    # check for whitespace
    whitespace_flag = 0
    for char in uname:
        if char in string.whitespace:
            whitespace_flag = 1
    # if whitespace, return error
    if whitespace_flag == 1: return -4

    users = getUsers()
    # Check against usernames
    if uname in users: return -3
    else: return 1

def passGen(size):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(size))


# Login to an existing account
def login():
    print(Fore.CYAN + "\n\n#=#=#=#=#=#=#=#=#=#=#=#=#")
    print(Fore.GREEN + "- Login to for PassVault -")
    print(Fore.CYAN + "#=#=#=#=#=#=#=#=#=#=#=#=#\n")

    # Ask for a username
    print(">>> Enter your username, or 'q' to cancel login")
    uname = input("@pv> ")

    # if the user chose to quit
    if uname == "q" or uname == "Q": return 1

    # Tell the user what went wrong and re-take input
    while(good_uname(uname) != -3 and uname != "q" and uname != "Q"):
        print(Fore.RED + "\n User does not exist!")
        print(">>> Enter your username, or 'q' to cancel login")
        uname = input("@pv> ")

    # if the user chose to quit
    if uname == "q" or uname == "Q": return 1

    # Fetch the user data
    salt, pw = fetchUserData(uname)

    # Ask for a password
    print(">>> Enter your password, or 'q' to cancel login")
    password = input("@pv> ")

    # if the user chose to quit
    if password == "q" or password == "Q": return 1

    # If the password is invalid, ask again
    while (crypto.checkPass(password, pw) == -1 and password != "q" and password != "Q"):
        print(Fore.RED + "\n Incorrect password!")
        print(">>> Enter your password, or 'q' to cancel login")
        password = input("@pv> ")

    # if the user chose to quit
    if password == "q" or password == "Q": return 1

    print(Fore.GREEN + "\n>>> Login successful!")
    return uname, salt


# Fetch all the user data
def fetchUserData(uname):
    salt = ""
    pw = ""
    flag = 0
    with open("users/users.txt", "r") as file:
        idx = 2;
        for line in file:
            idx += 1
            # If the username is a match, set the flag
            if idx % 3 == 0 and uname == line.strip() and flag != 1:
                flag = 1
            # Disable the flag
            elif idx % 3 == 0 and flag == 1:
                flag = 0
            # If the flag is set and this is the salt line
            if idx % 3 == 1 and flag == 1:
                salt = line.strip()
            # If the flag is set and this is the pw line
            elif idx % 3 == 2 and flag == 1:
                pw = line.strip()
    # return what was found, or report nothing
    if salt != "" and pw != "":
        return salt, pw
    else:
        return "NULL", "NULL"
