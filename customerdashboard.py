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
class CustomerDashboard:
    def _init_(self, master, user_id):
        self.window = tk.Toplevel(master)
        self.window.title("Customer Dashboard")
        self.window.geometry("600x400")
        
        conn = sqlite3.connect('hac.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        self.user = c.fetchone()
        conn.close()
        
        tk.Label(self.window, text=f"Welcome, {self.user[2]}!", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.window, text=f"Location: {self.user[5]}").pack()
        
        self.category = tk.StringVar()
        ttk.Combobox(self.window, textvariable=self.category,
                     values=["Select Category", "Tutor", "Photographer", "House Broker"]).pack(pady=10)
        self.category.set("Select Category")
        
        tk.Button(self.window, text="Search", command=self.search).pack(pady=10)
        
        self.results_frame = tk.Frame(self.window)
        self.results_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    
    def search(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if self.category.get() == "Select Category":
            tk.Label(self.results_frame, text="Please select a category to search").pack()
            return
        
        conn = sqlite3.connect('hac.db')
        c = conn.cursor()
        
        c.execute("""
            SELECT u.name, u.location, s.category, s.skills, s.contact_number
            FROM users u
            JOIN skill_holders s ON u.id = s.user_id
            WHERE u.location = ? AND s.category = ?
        """, (self.user[5], self.category.get()))
        
        results = c.fetchall()
        conn.close()
        
        if not results:
            tk.Label(self.results_frame, text=f"No {self.category.get()}s found in your area").pack()
        else:
            for result in results:
                frame = tk.Frame(self.results_frame, relief=tk.RAISED, borderwidth=1)
                frame.pack(fill=tk.X, padx=5, pady=5)
                tk.Label(frame, text=f"Name: {result[0]}").pack(anchor="w")
                tk.Label(frame, text=f"Location: {result[1]}").pack(anchor="w")
                tk.Label(frame, text=f"Category: {result[2]}").pack(anchor="w")
                tk.Label(frame, text=f"Skills: {result[3]}").pack(anchor="w")
                tk.Label(frame, text=f"Contact: {result[4]}").pack(anchor="w")
