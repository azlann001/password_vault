"""
shows all credentials stored with proper format
"""

import os
import hashlib
import base64
import bcrypt
import getpass
import json
from cryptography.fernet import Fernet



def view_pwd():
    while True:
        input_pwd = getpass.getpass("Enter master password (will be used for decryption key) : ")
        with open("m_pwd.txt", "rb") as f:
            stored_pwd = f.read()

        if bcrypt.checkpw(input_pwd.encode("UTF-8"), stored_pwd):
            break
        print("Error Wrong password try again...")

    key = derive_key(input_pwd)
    with open("vault.enc", "rb") as f:
        enc_dat = f.read()

    try:
        dec_dat = Fernet(key).decrypt(enc_dat)
    except Exception as e:
        print(f"Could not decrypt vault ({e}). File may be corrupted.")
        return

    data = json.loads(dec_dat)   # straight from memory, no temp file

    all_keys = set()        # showing the data

    if not data :
        print("\nuh-oh...Vault empty...")
        return

    for record in data:
        all_keys.update(record.keys())
    max_key_len = max(len(k) for k in all_keys)

    for serial, record in enumerate(data, start=1):
        print("[" + str(serial) + "]")
        for key, value in record.items():
            print("    " + key.ljust(max_key_len) + ": " + str(value))
        print()

    input("Press enter to exit...")
    clear_screen()



def derive_key( password ) :                # converts simple password to key which can be used by fernet for encrypting
    digest = hashlib.sha256(password.encode("UTF-8")).digest()          # first converts to bytes, then hashes and converts to 32bit 
    return base64.urlsafe_b64encode(digest)                     # converts to base 64 url safe password which fernet needs


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear") 

def del_file(path = "vault_view.json") :       
    os.remove(path)