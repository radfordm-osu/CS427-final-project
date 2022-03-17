import signup
import access
from colorama import init, Fore

def writeFile(name, content, make_if_null):
    return -1

def openFile(name):
    return 0

# Ask the user how to proceed
def startup():
    while (1):
        print(Fore.CYAN + "\n\n#=#=#=#=#=#=#=#=#=#=#=#=#")
        print(Fore.GREEN + "- Welcome to PassVault -")
        print(Fore.CYAN + "#=#=#=#=#=#=#=#=#=#=#=#=#\n")
        print(" 1- login (existing user)\n 2- sign up (new user)\n 3- exit\n")
        choice = input("@pv> ")
        # If the choice is not 1 or 2
        while (choice != "1" and choice != "2" and choice != "3"):
            print(Fore.RED + "\n That is not a valid option!")
            print(" 1- login (existing user)\n 2- sign up (new user)\n 3- exit\n")
            choice = input("@pv> ")

        if choice == "1":
            uname, pw = signup.login()
            # If the user chose to quit, continue
            if uname == pw == "":
                continue
            # Otherwise, play the access loop
            else:
                access.accessLoop(uname, pw)
        # If the user chose to sign up, playe the sign up loop
        elif choice == "2": signup.signup()
        # Otherwise, exit the program
        else: return 1

# The main function
def main():
    # init colorama
    init(autoreset=True)
    # use starting prompts
    status = startup()

    # Quit the program
    if status == 1:
        print(Fore.YELLOW + "\n\n#=#=#=#=#=#=#=#=#=#=#=#=#")
        print(Fore.RED + "      - Goodbye! -")
        print(Fore.YELLOW + "#=#=#=#=#=#=#=#=#=#=#=#=#\n\n")
        return 1

# call main on execution
if __name__ == "__main__":
    main()
