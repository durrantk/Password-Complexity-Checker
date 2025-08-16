import re
import math
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Optional: Try importing zxcvbn
try:
    from zxcvbn import zxcvbn
    zxcvbn_available = True
except ImportError:
    zxcvbn_available = False

# Load common passwords
def load_common_passwords(file_path='common-password.txt'):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return set(line.strip().lower() for line in f)

COMMON_PASSWORDS = load_common_passwords()

def password_entropy(password):
    charset = 0
    if re.search(r'[a-z]', password):
        charset += 26
    if re.search(r'[A-Z]', password):
        charset += 26
    if re.search(r'\d', password):
        charset += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        charset += 32
    return len(password) * math.log2(charset) if charset else 0

def time_to_crack(entropy):
    guesses = 2 ** entropy
    guesses_per_second = 10**9
    seconds = guesses / guesses_per_second
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"

def fallback_score(entropy):
    if entropy < 28:
        return 0
    elif entropy < 36:
        return 1
    elif entropy < 60:
        return 2
    elif entropy < 80:
        return 3
    else:
        return 4

def strength_metaphor(score):
    metaphors = {
        0: "As fragile as a house of cards in a hurricane (very weak)",
        1: " A wooden door with no lock (Weak)",
        2: " A locked door but with a known spare key (Medium)",
        3: " A steel vault with good locks (Strong)",
        4: " A mind fortress guarded by dragons (Very Strong)"
    }
    return metaphors.get(score, "Unknown strength")

def suggest_fixes(password):
    suggestions = []
    if len(password) < 8:
        suggestions.append("Use at least 8 characters.")
    if not re.search(r'[A-Z]', password):
        suggestions.append("Add uppercase letters.")
    if not re.search(r'[a-z]', password):
        suggestions.append("Add lowercase letters.")
    if not re.search(r'\d', password):
        suggestions.append("Include numbers.")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        suggestions.append("Use special characters.")
    if password.lower() in COMMON_PASSWORDS:
        suggestions.append("Avoid common or dictionary passwords.")
    return suggestions or ["No obvious weaknesses detected."]
    

# Main GUI function
def analyze_password_gui():
    password = entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    result_text.delete("1.0", tk.END)

    entropy = password_entropy(password)
    crack_time = time_to_crack(entropy)

    if zxcvbn_available:
        score = zxcvbn(password)['score']
    else:
        score = fallback_score(entropy)

    metaphor = strength_metaphor(score)
    suggestions = suggest_fixes(password)

    # Build result
    result = f" Entropy: {entropy:.2f} bits\n"
    result += f" Estimated time to crack: {crack_time}\n"
    result += f" Strength: {metaphor}\n\n"

    if password.lower() in COMMON_PASSWORDS:
       result_text.insert(tk.END, " This password is found in the common password list!\n\n", "red")
	
    result += " Suggestions to improve:\n"
    for s in suggestions:
        result += f"  - {s}\n"

    result_text.insert(tk.END, result)
    result_text.tag_config("red", foreground="red")
  

# GUI setup
window = tk.Tk()
window.title(" Password Strength Checker")
window.geometry("600x400")
window.resizable(False, False)

tk.Label(window, text="Enter your password:", font=("Arial", 12)).pack(pady=10)

entry = tk.Entry(window, width=40, font=("Arial", 12)) #add show='*' to add your the entered password 
entry.pack(pady=5)

tk.Button(window, text="Analyze Password", command=analyze_password_gui, font=("Arial", 12)).pack(pady=10)

result_text = scrolledtext.ScrolledText(window, width=70, height=15, font=("Consolas", 10))
result_text.pack(pady=10)

window.mainloop()

