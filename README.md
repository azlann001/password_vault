```
 _____                                    _   __      __         _ _
|  __ \                                  | |  \ \    / /        | | |
| |__) |_ _ ___ _____      _____  _ __ __| |   \ \  / /_ _ _   _| | |_
|  ___/ _` / __/ __\ \ /\ / / _ \| '__/ _` |    \ \/ / _` | | | | | __|
| |  | (_| \__ \__ \\ V  V / (_) | | | (_| |     \  / (_| | |_| | | |_
|_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|      \/ \__,_|\__,_|_|\__|
```

> **Class XII 2026 Summer Project** — Menu Driven, File Handling, Hashing & Password Encryption.

⎬ -------------------------------- ⎨

## Note -

**Master Password**

1. If someone (not you) changes your master password and you have data sotored then dont worry they cant access as it can only be access with the master password once set during setup.

2. If you want to change your master password , there's no direct way but you can do it by
   I. Writing the pasword TEMPORARILY in a text file
   II. Delete all stored data
   III. Selecting ( 1. Register Master Password ) and settign new master password
   IV. Adding your credentials again and deleting the temporary text file

3. And PLEASE do NOT forget the MASTER PASSWORD

⎬ -------------------------------- ⎨

## What You'll Need

1. **Python** installed on your computer (version 3.9 or newer).

Install Python from here: **[python.org/downloads](https://www.python.org/downloads/)**
While installing, **make sure to check the box that says "Add Python to PATH"** — this step is important, don't skip it.

⎬ -------------------------------- ⎨

## Setup Guide (One-Time Only)

### Step 1 — Extract the ZIP

**Extract** all files in the same folder.

### Step 2 — Open a terminal in that folder

- **Windows:** Right click on the folder where you stored all the files and click on **Open in terminal**

- **Mac:** Right click on the folder and click on **"New Terminal at Folder"**

- **Linux:** Right click on the folder and click on **Open in terminal**

You should now see a blinking cursor waiting for you to type.

### Step 3 — Install the required tools

Copy-paste this into the terminal and press Enter:

```
python -m pip install -r requirements.txt
```

This downloads a few small libraries the program needs (encryption tools, password hashing, clipboard support). Takes under a minute.

> If you see an error like `'pip' is not recognized`, try `pip3 install -r requirements.txt` instead.

### Step 4 — Run the program

```
python main.py
```

> If that doesn't work, try `python3 main.py` instead.

⎬ -------------------------------- ⎨

## How to Use It

The first time you run the program, u'll see:

```
1. Register Master Password
2. Login using Master Password
```

Choose **1** and set a Master Password.
**This is the password you must remember** — It's the key to access all the passwords u'll store, and yeah i know you will forget this too so keep it written on a piece of paper :>

Every time after that, choose **2** and enter your Master Password to log in.

Once logged in, you'll see the main menu:

| Option                          | What it does                                                                                                                         |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Add new password**         | Save a new website/app login (site, username, email, password, notes)                                                                |
| **2. View all entries**         | See everything saved in your vault                                                                                                   |
| **3. Edit entry**               | Change details of a saved entry (leave a field blank to keep it unchanged)                                                           |
| **4. Delete entry**             | Permanently remove a saved entry (asks for confirmation first)                                                                       |
| **5. Search your vault**        | Find an entry by site, username, email, or search everywhere at once                                                                 |
| **6. Generate strong password** | Create a secure random password, or one based on a keyword of your choice — pick one and it's copied to your clipboard automatically |
| **7. Check password strength**  | Type any password and get a strength score with tips to improve it                                                                   |
| **E**                           | Save and exit                                                                                                                        |

**Typing your password:** When the program asks for a password, your typing **won't show up on screen at all** — not even as dots. This is intentional (it's a security feature, not a bug) — just type normally and press Enter.

⎬ -------------------------------- ⎨

## How Your Data Is Protected

- Your Master Password is never stored directly — it's **hashed** using `bcrypt`, a one-way scrambling method. Not even the program itself can "look up" your original password.
- All your saved credentials are **encrypted** using `Fernet` (from the `cryptography` library) before being written to disk, using a key derived from your Master Password.
- The encrypted vault file (`vault.enc`) is unreadable gibberish to anyone without your Master Password.

⎬ -------------------------------- ⎨

## Files and Features

| File                   | Purpose                                                |
| ---------------------- | ------------------------------------------------------ |
| `main.py`              | Starts the program, handles login and the main menu    |
| `add_pwd.py`           | Add new credentials                                    |
| `view_pwd.py`          | View all saved credentials                             |
| `modify_pwd.py`        | Edit or delete credentials                             |
| `search_vault.py`      | Search saved credentials                               |
| `generate_password.py` | Generate strong passwords                              |
| `check_strength.py`    | Check how strong a password is                         |
| `requirements.txt`     | List of tools the program needs (used in Step 3 above) |

⎬ -------------------------------- ⎨

## Troubleshooting

**"No module named 'bcrypt'" (or similar)**
Step 3 didn't finish successfully. Try running `pip install -r requirements.txt` again and check for any red error text.

**"pip is not recognized"**
Try `pip3 install -r requirements.txt` instead, or `python -m pip install -r requirements.txt`.

**I closed the terminal — how do I run it again next time?**
Open a terminal inside the project folder again (Step 2), then run `python main.py` (Step 4). You don't need to repeat Step 3 (installing) again unless you move the folder to a different computer.

**I forgot my Master Password**
There is currently no recovery option — this is by design, since a recoverable master password would defeat the point of encryption. If forgotten, you'd need to delete `m_pwd.txt` and `vault.enc` and start fresh, losing previously saved entries.

⎬ -------------------------------- ⎨

## Built With

- Python 3
- [`bcrypt`](https://pypi.org/project/bcrypt/) — master password hashing
- [`cryptography`](https://pypi.org/project/cryptography/) (Fernet) — vault encryption
- [`pyperclip`](https://pypi.org/project/pyperclip/) — clipboard support for generated passwords
- `Coffee and late night debugging`
