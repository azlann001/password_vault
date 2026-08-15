"""
Search the vault by site, username, email, or across all fields.
Case-insensitive partial (substring) match.
"""

import os
import json
import getpass
import hashlib
import base64
import bcrypt
from cryptography.fernet import Fernet


def src_vlt():
    input_pwd = getpass.getpass("Enter master password : ")

    with open("m_pwd.txt", "rb") as f:
        stored_pwd = f.read()

    if not bcrypt.checkpw(input_pwd.encode("UTF-8"), stored_pwd):
        print("Error Wrong password try again...")
        src_vlt()
        return

    entries = load_vault(input_pwd)

    if not entries:
        print("Vault is empty. Nothing to search.")
        return

    field = choose_search_field()
    term = input("Enter search term : ").strip().lower()

    if term == "":
        print("Empty search term, cancelling.")
        return

    results = filter_entries(entries, field, term)

    if not results:
        print(f"\nNo matches found for '{term}'.")
        return

    print(f"\n{len(results)} match(es) found:\n")           # printing the results
    print_entries(results)
    input("\n\nPress enter to exit...")
    clear_screen()



def choose_search_field():
    print("\nSearch by:")
    print("1. Site")
    print("2. Username")
    print("3. Email")
    print("4. All fields")
    while True:
        ch = input("\nEnter your choice : ")
        if ch == "1":
            return "site"
        elif ch == "2":
            return "username"
        elif ch == "3":
            return "email"
        elif ch == "4":
            return "all"
        else:
            print("Invalid choice, try again.")


def filter_entries(entries, field, term): # Returns entries where the search term appears (case-insensitive substring) in the chosen field(s)
    matches = []
    for record in entries:
        if field == "all":
            # check across every value in the record, not just keys we know about
            haystack = " ".join(str(v) for v in record.values()).lower()
            if term in haystack:
                matches.append(record)
        else:
            value = str(record.get(field, "")).lower()
            if term in value:
                matches.append(record)
    return matches


def load_vault(master_pwd, enc_path="vault.enc"):       # Decrypts vault.enc and returns the list of entries. [] if missing/corrupted.
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


def print_entries(entries):     
    all_keys = set()
    for record in entries:
        all_keys.update(record.keys())
    max_key_len = max(len(k) for k in all_keys)

    for serial, record in enumerate(entries, start=1):
        print("[" + str(serial) + "]")
        for key, value in record.items():
            print("    " + key.ljust(max_key_len) + ": " + str(value))
        print()


def derive_key(password):
    digest = hashlib.sha256(password.encode("UTF-8")).digest()
    return base64.urlsafe_b64encode(digest)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear") 