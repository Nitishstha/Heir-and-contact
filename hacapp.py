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

    class HACApp:
     def _init_(self, master):
        self.master = master
        self.master.title("Hier and Contact (HAC)")
        self.master.geometry("400x300")
        self.create_db()
        self.create_main_window()
    
    def create_db(self):
        conn = sqlite3.connect('hac.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, user_type TEXT, name TEXT, email TEXT UNIQUE, 
                      password TEXT, location TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS skill_holders
                     (id INTEGER PRIMARY KEY, user_id INTEGER, category TEXT, skills TEXT,
                      contact_number TEXT, FOREIGN KEY(user_id) REFERENCES users(id))''')
        conn.commit()
        conn.close()
    
    def create_main_window(self):
        tk.Label(self.master, text="Welcome to Hier and Contact (HAC)", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self.master, text="Register", command=self.open_registration_window).pack(pady=10)
        tk.Button(self.master, text="Login", command=self.open_login_window).pack(pady=10)
    
    def open_registration_window(self):
        RegistrationWindow(self.master)
    
    def open_login_window(self):
        LoginWindow(self.master)
        