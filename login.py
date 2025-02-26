import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_placeholder(entry, placeholder_text):
    """Adds placeholder behavior to an entry widget."""
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')
    
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')
    
    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

class LoginWindow:
    def _init_(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Login")
        self.window.geometry("300x200")
        
        tk.Label(self.window, text="Login to HAC", font=("Helvetica", 16)).pack(pady=10)
        
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        
        entry_email = tk.Entry(self.window, textvariable=self.email)
        entry_email.pack(pady=5)
        add_placeholder(entry_email, "Email")
        
        entry_password = tk.Entry(self.window, textvariable=self.password, show="*")
        entry_password.pack(pady=5)
        add_placeholder(entry_password, "Password")
        
        tk.Button(self.window, text="Login", command=self.login).pack(pady=10)
    
    def login(self):
        conn = sqlite3.connect('hac.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (self.email.get(),))
        user = c.fetchone()
        conn.close()
        
        if user and user[4] == hash_password(self.password.get()):
            messagebox.showinfo("Success", "Login successful!")
            self.window.destroy()
            if user[1] == "Customer":
                CustomerDashboard(self.window.master, user[0])
            else:
                SkillHolderDashboard(self.window.master, user[0])
        else:
            messagebox.showerror("Error", "Invalid email or password")
