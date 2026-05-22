import re
import random
import string
import tkinter as tk
from tkinter import messagebox, ttk


def strength_meter(score):
    return score * 20


def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    if score == 5:
        level = "Strong"
    elif score >= 3:
        level = "Medium"
    else:
        level = "Weak"

    return level, score, feedback


def generate_password(length, use_numbers, use_uppercase, use_special):
    chars = string.ascii_lowercase

    if use_uppercase:
        chars += string.ascii_uppercase

    if use_numbers:
        chars += string.digits

    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    while True:
        password = "".join(random.choice(chars) for _ in range(length))
        level, score, _ = check_password_strength(password)

        if score >= 3:
            return password


class PasswordToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker & Generator")
        self.root.geometry("520x520")
        self.root.resizable(False, False)

        tk.Label(
            root,
            text="Password Strength Checker & Generator",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.check_frame = tk.Frame(notebook)
        self.generate_frame = tk.Frame(notebook)

        notebook.add(self.check_frame, text="Check Password")
        notebook.add(self.generate_frame, text="Generate Password")

        self.create_check_tab()
        self.create_generate_tab()

    def create_check_tab(self):
        tk.Label(self.check_frame, text="Enter Password:").pack(pady=10)

        self.password_entry = tk.Entry(self.check_frame, width=40, show="*")
        self.password_entry.pack(pady=5)

        self.show_password_var = tk.BooleanVar()

        tk.Checkbutton(
            self.check_frame,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password
        ).pack(pady=5)

        tk.Button(
            self.check_frame,
            text="Check Strength",
            command=self.check_password
        ).pack(pady=10)

        self.check_result_label = tk.Label(
            self.check_frame,
            text="Strength: ",
            font=("Arial", 12, "bold")
        )
        self.check_result_label.pack(pady=10)

        self.check_progress = ttk.Progressbar(
            self.check_frame,
            length=350,
            mode="determinate",
            maximum=100
        )
        self.check_progress.pack(pady=10)

        self.feedback_text = tk.Text(
            self.check_frame,
            height=8,
            width=50
        )
        self.feedback_text.pack(pady=10)

    def create_generate_tab(self):
        tk.Label(
            self.generate_frame,
            text="Password Length (8–20):"
        ).pack(pady=10)

        self.length_var = tk.IntVar(value=12)

        self.length_spinbox = tk.Spinbox(
            self.generate_frame,
            from_=8,
            to=20,
            textvariable=self.length_var,
            width=10
        )
        self.length_spinbox.pack(pady=5)

        self.use_numbers = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        tk.Checkbutton(
            self.generate_frame,
            text="Use Numbers",
            variable=self.use_numbers
        ).pack(pady=5)

        tk.Checkbutton(
            self.generate_frame,
            text="Use Mixed Uppercase/Lowercase",
            variable=self.use_uppercase
        ).pack(pady=5)

        tk.Checkbutton(
            self.generate_frame,
            text="Use Special Characters",
            variable=self.use_special
        ).pack(pady=5)

        tk.Button(
            self.generate_frame,
            text="Generate Password",
            command=self.generate_new_password
        ).pack(pady=15)

        self.generated_password_entry = tk.Entry(
            self.generate_frame,
            width=45
        )
        self.generated_password_entry.pack(pady=10)

        self.generate_result_label = tk.Label(
            self.generate_frame,
            text="Strength: ",
            font=("Arial", 12, "bold")
        )
        self.generate_result_label.pack(pady=10)

        self.generate_progress = ttk.Progressbar(
            self.generate_frame,
            length=350,
            mode="determinate",
            maximum=100
        )
        self.generate_progress.pack(pady=10)

        tk.Button(
            self.generate_frame,
            text="Copy Password",
            command=self.copy_password
        ).pack(pady=10)

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def check_password(self):
        password = self.password_entry.get()

        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return

        level, score, feedback = check_password_strength(password)
        percentage = strength_meter(score)

        self.check_result_label.config(text=f"Strength: {level} ({percentage}%)")
        self.check_progress["value"] = percentage

        self.feedback_text.delete("1.0", tk.END)

        if feedback:
            self.feedback_text.insert(tk.END, "Suggestions:\n\n")
            for tip in feedback:
                self.feedback_text.insert(tk.END, f"• {tip}\n")
        else:
            self.feedback_text.insert(tk.END, "Your password is strong.")

    def generate_new_password(self):
        length = self.length_var.get()

        if length < 8 or length > 20:
            messagebox.showerror("Error", "Length must be between 8 and 20.")
            return

        password = generate_password(
            length,
            self.use_numbers.get(),
            self.use_uppercase.get(),
            self.use_special.get()
        )

        level, score, _ = check_password_strength(password)
        percentage = strength_meter(score)

        self.generated_password_entry.delete(0, tk.END)
        self.generated_password_entry.insert(0, password)

        self.generate_result_label.config(text=f"Strength: {level} ({percentage}%)")
        self.generate_progress["value"] = percentage

    def copy_password(self):
        password = self.generated_password_entry.get()

        if not password:
            messagebox.showerror("Error", "No password generated.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordToolGUI(root)
    root.mainloop()