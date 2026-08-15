"""
Lets the user view all credentials, pick one by serial number,
and update its fields. Blank input on a field keeps the old value.
"""

import os
import json
import getpass
import hashlib
import base64
import bcrypt
from cryptography.fernet import Fernet


def edit_pwd():
    input_pwd = getpass.getpass("Enter master password : ")             # takes master password


    with open("m_pwd.txt", "rb") as f:          # gets the saved master password hash
        stored_pwd = f.read()

    if not bcrypt.checkpw(input_pwd.encode("UTF-8"), stored_pwd):       # checks master password with entered one
        print("Error Wrong password try again...")
        edit_pwd()
        return

    entries = load_vault(input_pwd)             

    if not entries:
        print("Vault is empty. Nothing to edit.")
        return

    print_entries(entries)

    index = get_valid_index(len(entries))
    if index is None:          # user typed 0 to cancel
        return

    record = entries[index]
    print(f"\nEditing entry [{index + 1}] — leave blank to keep current value.\n")

    new_site = input(f"Site [{record['site']}] : ")
    record["site"] = new_site if new_site != "" else record["site"]

    new_username = input(f"Username [{record['username']}] : ")
    record["username"] = new_username if new_username != "" else record["username"]

    new_email = input(f"Email [{record['email']}] : ")
    record["email"] = new_email if new_email != "" else record["email"]

    new_password = getpass.getpass("Password [leave blank to keep current] : ")
    record["password"] = new_password if new_password != "" else record["password"]

    new_notes = input(f"Notes [{record['notes']}] : ")
    record["notes"] = new_notes if new_notes != "" else record["notes"]

    save_plain(entries)
    encrypt_file(input_pwd)
    del_plain_file()
    print("Entry updated and saved.")


def load_vault(master_pwd, enc_path="vault.enc"):   #Decrypts vault.enc and returns the list of entries. [] if missing/corrupted
    
    key = derive_key(master_pwd)
    try:
        with open(enc_path, "rb") as f:
            token = f.read()
    except FileNotFoundError:
        return []
    try:
        plain_bytes = Fernet(key).decrypt(token)
        return json.loads(plain_bytes)
    except Exception as e:
        print(f"Could not decrypt vault ({e}).")
        return []


def print_entries(entries):         # prints all the saved entries
    all_keys = set()
    for record in entries:
        all_keys.update(record.keys())
    max_key_len = max(len(k) for k in all_keys)

    for serial, record in enumerate(entries, start=1):
        print("[" + str(serial) + "]")
        for key, value in record.items():
            print("    " + key.ljust(max_key_len) + ": " + str(value))
        print()


def get_valid_index(count):         # gets the index from user for editing / deleting
    """Prompts for a serial number, returns 0-based index, or None if user cancels."""
    while True:
        raw = input(f"Enter the serial number to edit (1-{count}, or 0 to cancel) : ")
        if raw == "0":
            return None
        if raw.isdigit() and 1 <= int(raw) <= count:
            return int(raw) - 1
        print(f"Invalid choice. Enter a number between 1 and {count}, or 0 to cancel.")


def derive_key(password):       # makes the master password readable for fernet
    digest = hashlib.sha256(password.encode("UTF-8")).digest()
    return base64.urlsafe_b64encode(digest)


def save_plain(data_in_list, file_name="vault_plain.json"):
    with open(file_name, "w") as file:
        json.dump(data_in_list, file, indent=5)


def encrypt_file(master_pwd, plain_path="vault_plain.json", enc_path="vault.enc"):
    key = derive_key(master_pwd)
    with open(plain_path, "rb") as p_file:
        p_data = p_file.read()
    token = Fernet(key).encrypt(p_data)

    with open(enc_path, "wb") as e_file:      # overwrite, not append — same fix as add_pwd.py
        e_file.write(token)


def del_plain_file(plain_path="vault_plain.json"):
    os.remove(plain_path)





    

def delete_pwd():
    input_pwd = getpass.getpass("Enter master password : ")         # takes master password

    with open("m_pwd.txt", "rb") as f:              # gets the saved master password hash
        stored_pwd = f.read()

    if not bcrypt.checkpw(input_pwd.encode("UTF-8"), stored_pwd):           # checks master password with entered one
        print("Error Wrong password try again...")
        delete_pwd()
        return

    entries = load_vault(input_pwd)

    if not entries:
        print("Vault is empty. Nothing to delete.")
        return

    print_entries(entries)

    index = get_valid_index(len(entries))
    if index is None:                    # user typed 0 to cancel
        return

    record = entries[index]             
    print(f"\nYou are about to delete entry [{index + 1}] — site: {record['site']}, username: {record['username']}")
    confirm = input("Type 'y' to confirm deletion, anything else to cancel : ")

    if confirm.lower() != "y":
        print("Deletion cancelled.")
        return

    entries.pop(index)

    save_plain(entries)
    encrypt_file(input_pwd)
    del_plain_file()
    print("Entry deleted and vault updated.")
