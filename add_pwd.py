""" 
basic structure of the entries -
entry = {
            "site" : ""
            "username" : ""
            "email" : ""
            "password" : ""
            "notes" : ""
}

"""


import os
import json
import getpass
import hashlib
import base64
import bcrypt
from cryptography.fernet import Fernet


def add_pwd_main():
    entries = []
    master_pwd = None  # cached for the session so we don't re-prompt on every add

    # --- Load existing vault once, at startup ---
    if os.path.exists("vault.enc"):
        master_pwd = authenticate()          # verifies against m_pwd.txt, returns the raw password
        entries = load_vault(master_pwd)     # decrypt + json.loads, or [] if that fails

    while True:
        print("1. Add Credentials...")
        print("0. Exit...")
        ch = input("Enter your choice : ")

        if ch == "1":
            if master_pwd is None:
                master_pwd = authenticate()  # first entry ever, vault didn't exist yet
            print("\nEnter your credentials...\n")
            temp = {
                "site": input("Enter the site name : "),
                "username": input("Enter your username : "),
                "email": input("Enter your email : "),
                "password": getpass.getpass("Enter your password : "),
                "notes": input("Enter notes : "),
            }
            entries.append(temp)

            save_plain(entries)
            encrypt_file(master_pwd)   # always overwrites — entries already has full history
            del_plain_file()

        elif ch == "0":
            print("Changes saved...")
            break
        else:
            print("Wrong Choice try again...")


def authenticate():
    """Prompt + verify master password against the stored bcrypt hash. Returns the raw password on success."""
    while True:
        input_pwd = getpass.getpass("Enter master password : ")
        with open("m_pwd.txt", "rb") as f:
            stored_pwd = f.read()
        if bcrypt.checkpw(input_pwd.encode("UTF-8"), stored_pwd):
            return input_pwd
        print("Error Wrong password try again...")


def derive_key(password):
    digest = hashlib.sha256(password.encode("UTF-8")).digest()
    return base64.urlsafe_b64encode(digest)


def load_vault(master_pwd, enc_path="vault.enc"):
    """Decrypt vault.enc and return the list of entries. Empty list if anything goes wrong."""
    key = derive_key(master_pwd)
    try:
        with open(enc_path, "rb") as f:
            token = f.read()
        plain_bytes = Fernet(key).decrypt(token)   # will raise InvalidToken if corrupted/wrong key
        return json.loads(plain_bytes)
    except FileNotFoundError:
        return []
    except Exception as e:
        # InvalidToken (wrong password / corrupted file) or JSONDecodeError
        print(f"Could not read existing vault ({e}). Starting fresh — check your file/password.")
        return []


def save_plain(data_in_list, file_name="vault_plain.json"):
    with open(file_name, "w") as file:
        json.dump(data_in_list, file, indent=5)


def encrypt_file(master_pwd, plain_path="vault_plain.json", enc_path="vault.enc"):
    key = derive_key(master_pwd)
    with open(plain_path, "rb") as p_file:
        p_data = p_file.read()
    token = Fernet(key).encrypt(p_data)

    # ALWAYS overwrite — p_data already contains the full, up-to-date entries list
    with open(enc_path, "wb") as e_file:
        e_file.write(token)


def del_plain_file(plain_path="vault_plain.json"):
    os.remove(plain_path)