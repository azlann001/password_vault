"""

Note - Run this file in Terminal 


 Master Password - A password registered and stored for a user to access all files and stored passwords

 Note - Choosing "Register Master Password" again would reset the Master Password and you wont be able to access the stored data unless you change the password again back to the original one.

"""

import bcrypt
import getpass
import add_pwd
import view_pwd
import modify_pwd
import search_vault
import generate_password
import check_strength


#print("✕⎯⎯⎯⎯⎯"*20,"\b✕")



def main_login() :    # main funcion for the login process



    def register_m_pwd() :  # function to register password

        password = getpass.getpass("Enter Master Password : ").encode("UTF-8")    # inputting master password
        print("\n\nNote- If you forget passwords which i believe you do...please write this one one piece of paper and keep it safe :)...\n\n")
        hashed = bcrypt.hashpw(password , bcrypt.gensalt())             # hashing master password to store
    
    
        with open("m_pwd.txt" , "bw+") as f :                            # storing hashed master password to a file
            f.write(hashed)
            
    
            def chk_pw():                       # confirming the entered password is the right password or if the uer wants to change it 

                f.seek(0)                       # puts the file pointer at the start of file so it reads from start everytime

                ch = input("Do you want to make changes to the Password ? y/n : ")

                if ch in "yY" :
                    register_m_pwd()               

                else :
                    temp = getpass.getpass("Enter Password to confirm : ").encode("UTF-8")
                    if bcrypt.checkpw(temp , f.read() ) :
                        print("Success password matched...")
                    else :
                        print("Wrong password enter again...")
                        chk_pw()
            chk_pw()    
        login()





    def login() :
        pw = getpass.getpass("Enter your Master Password to login : ").encode("UTF-8")
        with open ("m_pwd.txt" , "br" ) as f :
            f.seek(0)
            if bcrypt.checkpw( pw , f.read() ) :
                print("Password Matched...")
                main_display()
                
            else :
                print("Incorrect password Try again...")
                login()





    def menu() :                    # goes inside main_display() 
        print("\n\n" , "✕¯_¯_¯_"*10,"\b✕")
        print( "\n" , " "*15 , "Your Personal Password Vault " )
        print("1. Add new password ")
        print("2. View all entries ")
        print("3. Edit entry ")
        print("4. Delete entry ")
        print("5. Search your vault ")
        print("6. Generate strong Passowrd ")
        print("7. Check password strength ")
        print("E/e. Exit")
        print("\n\n" , "✕¯_¯_¯_"*10,"\b✕")

    



    def main_display() :                    # displayed after login 

        while True :
            menu()
            choice = input("\nEnter your choice : ")
            if choice == "1" :
                add_pwd.add_pwd_main()
            elif choice == "2" :
                view_pwd.view_pwd()
            elif choice == "3" :
                modify_pwd.edit_pwd()
            elif choice == "4" :
                modify_pwd.delete_pwd()
            elif choice == "5" :
                search_vault.src_vlt()
            elif choice == "6" :
                generate_password.pwd_generator()
            elif choice == "7" :
                check_strength.strength_checker()
            elif choice == "E" or choice == "e" :
                print("Changes saved...\n")
                break
            else :
                print("Error...Invalid choice try again...")

    def print_banner():
        banner = r"""
 ____   _    ____ ______        _____  ____  ____    __     __   _   _   _ _   _____
|  _ \ / \  / ___/ ___\ \      / / _ \|  _ \|  _ \   \ \   / /  / \ | | | | | |_   _|
| |_) / _ \ \___ \___ \\ \ /\ / / | | | |_) | | | |   \ \ / /  / _ \| | | | |   | |
|  __/ ___ \ ___) |__) |\ V  V /| |_| |  _ <| |_| |    \ V /  / ___ \ |_| | |___| |
|_| /_/   \_\____/____/  \_/\_/  \___/|_| \_\____/      \_/  /_/   \_\___/|_____|_|
    """
        print(banner)



    print("✕⎯⎯⎯⎯⎯"*10,"\b✕\n")
    print_banner()
    print("1. Register Master Password")
    print("2. Login using Master Password")

    choice = input("Enter your choice...")

    if choice == "1" :
        register_m_pwd()

       
    elif choice == "2" :

        try :
            with open( "m_pwd.txt" , "rb" ) as f :
                f.read()
        except :
            print("\nPlease register first...\n")
            register_m_pwd()
        else :
            login()
    


    print("✕⎯⎯⎯⎯⎯"*10,"\b✕")



main_login()
