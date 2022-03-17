import crypto
from colorama import init, Fore
import string
import random
import os

# This file will contain the user process
# to actually access and save data
def accessLoop(user, pw):
    print(Fore.CYAN + "\n\n#=#=#=#=#=#=#=#=#=#=#=#=#")
    print(Fore.GREEN + "- Welcome, " + user + " -")
    print(Fore.CYAN + "#=#=#=#=#=#=#=#=#=#=#=#=#")
    while(1):
        print("\n 1- add service (existing user)\n 2- edit service\n 3- remove service\n 4- view service names\n 5- view data for a service\n 6- logout")
        choice = input("@pv> ")
        # If the choice is not 1 or 2
        while (choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5" and choice != "6"):
            print(Fore.RED + "\n That is not a valid option!")
            print("\n 1- add service (existing user)\n 2- edit service\n 3- remove service\n 4- view service names\n 5- view data for a service\n 6- logout")
            choice = input("@pv> ")
        if choice == "1":
            add_service(user, pw)
        elif choice == "2":
            change_service(user, pw)
        elif choice == "3":
            delete_service(user, pw)
        elif choice == "4":
            print_services(user, pw)
        elif choice == "5":
            print_service_data(user, pw)
        # Log the user out
        elif choice == "6":
            return 1

# This function will prompt the user to create a new service
# and write the data to a file
def add_service(user, pw):
    # If the user chooses to quit, close this
    s_name = get_service_name()
    if (s_name == "q" or s_name == "3"):
        return 1

    # If the user chooses to quit, close this
    u_name = get_user_name(s_name)
    if (u_name == "q" or u_name == "3"):
        return 1

    # If the user chooses to quit, close this
    p_word = get_password(s_name)
    if (p_word == "q" or p_word == "3"):
        return 1

    # Open the user file and get the existing data
    lines = ""
    ufile = open("users/" + user + ".txt", "r")
    for line in ufile:
        lines = lines + line

    # Close the file and report back
    ufile.close()

    print(Fore.CYAN + "\n >>> Processing. Please wait...\n")

    if lines != "":
        dec_lines = crypto.decrypt(pw, lines, user)
    else:
        dec_lines = ""

    # Append to the end
    dec_lines = dec_lines + s_name + "\n" + u_name + "\n" + p_word + "\n"

    enc_lines = crypto.encrypt(pw, dec_lines, user)

    # Overwrite the file contents
    ufile = open("users/" + user + ".txt", "w")
    ufile.write(enc_lines)
    ufile.close()

    print(Fore.GREEN + "\n Data saved for service: " + s_name)
    return 1


# This function will ask a user to change data for a service
# And update the data
def change_service(user, pw):

    ptxt = get_file_data(user, pw, 1)

    # If the user chooses to quit, close this
    s_name = get_service_name()
    if (s_name == "q" or s_name == "3"):
        return 1

    # Parse the data
    idx = 2
    s_name_exists = False
    lines = []
    flag = 0
    for line in ptxt:
        idx += 1
        # If the service name is a match, set the flag

        if idx % 3 == 0 and s_name == line.strip() and flag != 1:
            flag = 1
            s_name_exists = True
        # Disable the flag
        elif idx % 3 == 0 and flag == 1:
            flag = 0
        # If the flag is not set, copy the line into an array
        if flag == 0:
            lines.append(line.strip())
        # Otherwise, append a placeholder
        else:
            lines.append("")

    # If a service is not there
    if s_name_exists == False:
        print(Fore.RED + "\n Service '" + s_name + "' does not exist!\n")
        return 1
    # If the user chooses to quit, close this
    u_name = get_user_name(s_name)
    if (u_name == "q" or u_name == "3"):
        return 1

    # If the user chooses to quit, close this
    p_word = get_password(s_name)
    if (p_word == "q" or p_word == "3"):
        return 1

    cnt = -1
    final = ""
    # Re-write the lines
    for line in lines:
        # If this is a slot to re-write
        if len(line) == 0:
            cnt += 1
            if cnt == 0:
                final += s_name+"\n"
            elif cnt == 1:
                final += u_name+"\n"
            elif cnt == 2:
                final += p_word+"\n"
        # Otherwise, append the old content
        else:
            final += line.strip() + "\n"

    print(Fore.CYAN + "\n >>> Processing. Please wait...\n")

    ctxt = crypto.encrypt(pw, final, user)
    ufile = open("users/" + user + ".txt", "w")
    ufile.write(ctxt)

    ufile.close()
    print(Fore.GREEN + "\n Data saved for service: " + s_name)
    return 1


# Delete a service for a user
def delete_service(user, pw):

    ptxt = get_file_data(user, pw, 1)

    # If the user chooses to quit, close this
    s_name = get_service_name()
    if (s_name == "q" or s_name == "3"):
        return 1

    # Find the lines
    idx = 2
    s_name_exists = False
    lines = []
    flag = 0
    final = ""
    for line in ptxt:
        idx += 1
        # If the service name is a match, set the flag
        if idx % 3 == 0 and s_name == line.strip() and flag != 1:
            flag = 1
            s_name_exists = True
        # Ignore the line
        if flag == 1:
            # Reset the flag
            if idx % 3 == 2:
                flag = 0
        # Copy the line
        else:
            final = final + line.strip() + "\n"

    final = final[:-1]

    # If the service is not defined for this user, report and return
    if s_name_exists == False:
        print(Fore.RED + "\n Service '" + s_name + "' does not exist!\n")
        return 1

    print(Fore.CYAN + "\n >>> Processing. Please wait...\n")

    if final != "":
        # Re-encrypt everything
        ctxt = crypto.encrypt(pw, final, user)
    else:
        ctxt = ""

    # Open the user file
    ufile = open("users/" + user + ".txt", "w")
    ufile.write(ctxt)
    ufile.close()
    print(Fore.GREEN + "\n Removed data for service: " + s_name + "\n")
    return 1


# Print all service names for a user
def print_services(user, pw):
    ptxt = get_file_data(user, pw, 1)
    idx = 2
    s_name_exists = False
    names = []
    for line in ptxt:
        idx += 1
        # If this is a service name, keep it
        if idx % 3 == 0:
            names.append(line.strip())

    print(Fore.CYAN + "\n\n#=#=#=#=#=#=#=#=#=#=#=#=#")
    print(Fore.GREEN + "- Service names for " + user + " -")
    print(Fore.CYAN + "#=#=#=#=#=#=#=#=#=#=#=#=#")
    loop = 1
    for name in names:
        if (name != ""):
            print("\n " + str(loop) + "- " + name)
        loop += 1
    print("\n")
    return 1


def print_service_data(user, pw):

    ptxt = get_file_data(user, pw, 1)


    # If the user chooses to quit, close this
    s_name = input_service_name()
    if (s_name == "q" or s_name == "3"):
        return 1

    idx = 2
    s_name_exists = False
    lines = []
    flag = 0
    for line in ptxt:
        idx += 1
        # Disable the flag
        if idx % 3 == 0 and flag == 1:
            flag = 0
        # If the service name is a match, set the flag
        if idx % 3 == 0 and s_name == line.strip() and flag != 1:
            flag = 1
            s_name_exists = True
        # If the flag is set
        if flag == 1:
            if idx % 3 == 1:
                u_name = line.strip()
            if idx % 3 == 2:
                p_word = line.strip()

    # If the service is not defined for this user, report and return
    if s_name_exists == False:
        print(Fore.RED + "\n Service '" + s_name + "' does not exist!\n")
        return 1

    print(Fore.CYAN + "\n\n#=#=#=#=#=#=#=#=#=#=#=#=#")
    print(Fore.GREEN + "- Data for " + s_name + " -")
    print(Fore.CYAN + "#=#=#=#=#=#=#=#=#=#=#=#=#")
    print("\n USERNAME: " + u_name)
    print(" PASSWORD: " + p_word + "\n")
    return 1


# Get the service name from the user
def input_service_name():
    # Ask for the service name
    print("\n What is the service name? (Type 'q' to cancel)")
    s_name = input("@pv> ")
    # Cancel if user inputs 'q'
    if s_name == "q":
        return "q"
    # Otherwise return the service name
    return s_name


# Get the service name from the user
def get_service_name():
    verify_name = "0"
    # Ask for the service name
    while (verify_name != "1" and verify_name != "3"):
        print("\n What is the service name? (Type 'q' to cancel)")
        s_name = input("@pv> ")
        # Cancel if user inputs 'q'
        if s_name == "q":
            return "q"
        # Verify the service name with the user
        print("\n You are changing data for: '" + s_name + "'.\n 1- accept\n 2- change\n 3- cancel\n")
        verify_name = input("@pv> ")
        # Loop for invalid input
        while (verify_name != "1" and verify_name != "2" and verify_name != "3"):
            print(Fore.RED + "\nThat is not an option!")
            print("\n You are changing data for: '" + s_name + "'.\n 1- accept\n 2- change\n 3- cancel\n")
            verify_name = input("@pv> ")
    # If the user is cancelling, return "3"
    if verify_name == "3": return "3"
    # Otherwise return the service name
    return s_name


# Get the username for a service
def get_user_name(s_name):
    verify_usr = "0"
    # Ask for the username
    while (verify_usr != "1" and verify_usr != "3"):
        print("\n What is your username for " + s_name + "? (Input 'q' to cancel)")
        u_name = input("@pv> ")
        # Cancel if user inputs 'q'
        if u_name == "q":
            return "q"
        # Verify uname with user
        print("\n Your username for " + s_name + " is '" + u_name + "'\n 1- accept\n 2- change\n 3- cancel\n")
        verify_usr = input("@pv> ")
        # Loop on bad input
        while (verify_usr != "1" and verify_usr != "2" and verify_usr != "3"):
            print(Fore.RED + "\nThat is not an option!")
            print("\n Your username for " + s_name + " is '" + u_name + "'\n 1- accept\n 2- change\n 3- cancel\n")
            verify_usr = input("@pv> ")
    # If the user is cancelling, return "3"
    if verify_usr == "3": return "3"
    # Otherwise return the service name
    return u_name


# Get the username for a service
def get_password(s_name):
    verify_usr = "0"
    # Ask for the username
    while (verify_usr != "1" and verify_usr != "3"):
        print("\n What is your password for " + s_name + "? (Input 'q' to cancel)")
        pw = input("@pv> ")
        # Cancel if user inputs 'q'
        if pw == "q":
            return "q"
        # Verify uname with user
        print("\n Your password for " + s_name + " is '" + pw + "'\n 1- accept\n 2- change\n 3- cancel\n")
        verify_usr = input("@pv> ")
        # Loop on bad input
        while (verify_usr != "1" and verify_usr != "2" and verify_usr != "3"):
            print(Fore.RED + "\nThat is not an option!")
            print("\n Your password for " + s_name + " is '" + pw + "'\n 1- accept\n 2- change\n 3- cancel\n")
            verify_usr = input("@pv> ")
    # If the user is cancelling, return "3"
    if verify_usr == "3": return "3"
    # Otherwise return the service name
    return pw

def get_file_data(user, pw, mode):

    print(Fore.CYAN + "\n >>> Processing. Please wait...\n")

    # Open the user file and get the existing data
    lines = ""
    ufile = open("users/" + user + ".txt", "r")
    for line in ufile:
        lines = lines + line
    # Close the file and report back
    ufile.close()

    if lines != "":
        dec_lines = crypto.decrypt(pw, lines, user)
    else:
        dec_lines = ""
    if mode == 0:
        return dec_lines
    else:
        final_lines = []
        final_lines = dec_lines.split("\n")
        return final_lines
