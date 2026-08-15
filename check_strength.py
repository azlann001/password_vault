"""
Checks password strength using length, character variety, and pattern detection.
Gives a score, a rating label, and specific actionable feedback.
"""

import string

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "letmein",
    "monkey", "111111", "admin", "welcome", "password1"
}


def strength_checker():
    pwd = input("Enter the password to check : ")

    if pwd == "":
        print("Password can't be empty.")
        return

    score, feedback = evaluate(pwd)
    rating = score_to_rating(score)

    print(f"\nStrength: {rating}  ({score}/100)")
    if feedback:
        print("\nSuggestions:")
        for f in feedback:
            print(f" - {f}")
    else:
        print("No issues found. This is a strong password.")


def evaluate(pwd):
    score = 0
    feedback = []

    # --- Length (up to 40 points) ---
    length = len(pwd)
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
        feedback.append("Consider using 16+ characters for stronger protection.")
    elif length >= 8:
        score += 15
        feedback.append("Password is a bit short — aim for 12+ characters.")
    else:
        feedback.append("Password is too short (under 8 characters) — very easy to brute-force.")

    # --- Character variety (up to 40 points, 10 each) ---
    has_lower = any(c in string.ascii_lowercase for c in pwd)
    has_upper = any(c in string.ascii_uppercase for c in pwd)
    has_digit = any(c in string.digits for c in pwd)
    has_special = any(c in string.punctuation for c in pwd)

    variety_count = sum([has_lower, has_upper, has_digit, has_special])
    score += variety_count * 10

    if not has_lower:
        feedback.append("Add lowercase letters.")
    if not has_upper:
        feedback.append("Add uppercase letters.")
    if not has_digit:
        feedback.append("Add numbers.")
    if not has_special:
        feedback.append("Add special characters (e.g. ! @ # $).")

    # --- Common password check (heavy penalty) ---
    if pwd.lower() in COMMON_PASSWORDS:
        score = min(score, 5)     # cap score hard regardless of length/variety
        feedback.append("This is a commonly used password — extremely easy to guess.")

    # --- Sequential characters (e.g. abc, 123, qwerty-order) ---
    if has_sequential_run(pwd, run_length=3):
        score -= 15
        feedback.append("Avoid sequential characters like 'abc' or '123'.")

    # --- Repeated characters (e.g. aaa, 111) ---
    if has_repeated_run(pwd, run_length=3):
        score -= 15
        feedback.append("Avoid repeating the same character multiple times in a row.")

    score = max(0, min(100, score))   # clamp into 0-100
    return score, feedback


def has_sequential_run(pwd, run_length=3):
    """Detects ascending or descending runs of consecutive characters (by char code)."""
    for i in range(len(pwd) - run_length + 1):
        window = pwd[i:i + run_length]
        codes = [ord(c) for c in window]
        ascending = all(codes[j] + 1 == codes[j + 1] for j in range(len(codes) - 1))
        descending = all(codes[j] - 1 == codes[j + 1] for j in range(len(codes) - 1))
        if ascending or descending:
            return True
    return False


def has_repeated_run(pwd, run_length=3):
    """Detects the same character repeated run_length or more times in a row."""
    count = 1
    for i in range(1, len(pwd)):
        if pwd[i] == pwd[i - 1]:
            count += 1
            if count >= run_length:
                return True
        else:
            count = 1
    return False


def score_to_rating(score):
    if score >= 80:
        return "Very Strong"
    elif score >= 60:
        return "Strong"
    elif score >= 35:
        return "Fair"
    else:
        return "Weak"