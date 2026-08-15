"""
Generates strong passwords two ways:
  1. Fully random (max entropy, no memorability)
  2. Keyword-based (user's word + leetspeak + random padding)
Lets the user pick one from a list and copies it to the clipboard.
"""

import os
import secrets
import string

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


LEET_MAP = {
    "a": "@", "e": "3", "i": "1", "o": "0", "s": "$", "t": "7"
}


def pwd_generator():
    print("\n1. Generate random secure password...")
    print("2. Generate password with a keyword by providing it...")
    ch = input("Enter your choice : ")

    if ch == "1":
        length = get_valid_length()
        options = [random_password(length) for _ in range(5)]
    elif ch == "2":
        keyword = input("Enter a keyword to include : ").strip()
        if keyword == "":
            print("Keyword can't be empty.")
            return
        length = get_valid_length(min_len=len(keyword) + 4)
        options = [keyword_password(keyword, length) for _ in range(5)]
    else:
        print("Invalid choice.")
        return

    show_and_select(options)


def get_valid_length(min_len=8):
    while True:
        raw = input(f"Enter desired password length (min {min_len}, default 16) : ").strip()
        if raw == "":
            return max(16, min_len)
        if raw.isdigit() and int(raw) >= min_len:
            return int(raw)
        print(f"Enter a number >= {min_len}.")


def random_password(length):
    """Cryptographically secure fully random password from a large character pool."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


def keyword_password(keyword, length):
    """
    Builds a password containing the user's keyword, but:
      - randomly leetspeaks some letters
      - randomizes casing
      - pads with random characters on both sides so the keyword
        isn't sitting at a predictable position (start/end)
    """
    transformed = []
    for ch in keyword:
        if ch.lower() in LEET_MAP and secrets.randbelow(2):   # ~50% chance to leetspeak each eligible letter
            transformed.append(LEET_MAP[ch.lower()])
        else:
            transformed.append(ch.upper() if secrets.randbelow(2) else ch.lower())
    core = "".join(transformed)

    pad_total = max(0, length - len(core))
    pad_left_len = secrets.randbelow(pad_total + 1)     # random split of padding on each side
    pad_right_len = pad_total - pad_left_len

    alphabet = string.ascii_letters + string.digits + string.punctuation
    pad_left = "".join(secrets.choice(alphabet) for _ in range(pad_left_len))
    pad_right = "".join(secrets.choice(alphabet) for _ in range(pad_right_len))

    return pad_left + core + pad_right


def show_and_select(options):
    print("\nGenerated options:\n")
    for i, pwd in enumerate(options, start=1):
        print(f"[{i}] {pwd}")

    while True:
        raw = input(f"\nPick one to copy (1-{len(options)}, or 0 to cancel) : ")
        if raw == "0":
            clear_screen()
            return
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            chosen = options[int(raw) - 1]
            copy_to_clipboard(chosen)
            input("Press enter to continue...")
            clear_screen()
            return
        print("Invalid choice.")

        
        


def copy_to_clipboard(password):
    if CLIPBOARD_AVAILABLE:
        pyperclip.copy(password)
        print("Copied to clipboard.")
    else:
        print("pyperclip not installed — here's your password (copy manually):")
        print(password)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear") 