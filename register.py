
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
    
    class RegistrationWindow:
     def _init_(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Register")
        self.window.geometry("400x500")
        
        tk.Label(self.window, text="Register for HAC", font=("Helvetica", 16)).pack(pady=10)
        
        self.user_type = tk.StringVar()
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.location = tk.StringVar()
        self.category = tk.StringVar()
        self.skills = tk.StringVar()
        self.contact_number = tk.StringVar()
        
        ttk.Combobox(self.window, textvariable=self.user_type, values=["Customer", "Skill Holder"]).pack(pady=5)
        
        entry_name = tk.Entry(self.window, textvariable=self.name)
        entry_name.pack(pady=5)
        add_placeholder(entry_name, "Name")
        
        entry_email = tk.Entry(self.window, textvariable=self.email)
        entry_email.pack(pady=5)
        add_placeholder(entry_email, "Email")
        
        entry_password = tk.Entry(self.window, textvariable=self.password, show="*")
        entry_password.pack(pady=5)
        add_placeholder(entry_password, "Password")
        
        entry_location = tk.Entry(self.window, textvariable=self.location)
        entry_location.pack(pady=5)
        add_placeholder(entry_location, "Location")
        
        self.skill_holder_frame = tk.Frame(self.window)
        ttk.Combobox(self.skill_holder_frame, textvariable=self.category,
                     values=["Tutor", "Photographer", "House Broker"]).pack(pady=5)
        
        entry_skills = tk.Entry(self.skill_holder_frame, textvariable=self.skills)
        entry_skills.pack(pady=5)
        add_placeholder(entry_skills, "Skills (comma-separated)")
        
        entry_contact = tk.Entry(self.skill_holder_frame, textvariable=self.contact_number)
        entry_contact.pack(pady=5)
        add_placeholder(entry_contact, "Contact Number")
        
        self.user_type.trace('w', self.toggle_skill_holder_fields)
        
        tk.Button(self.window, text="Register", command=self.register).pack(pady=10)
    
    def toggle_skill_holder_fields(self, *args):
        if self.user_type.get() == "Skill Holder":
            self.skill_holder_frame.pack(pady=10)
        else:
            self.skill_holder_frame.pack_forget()
    
    def register(self):
        conn = sqlite3.connect('hac.db')
        c = conn.cursor()
        try:
            hashed_password = hash_password(self.password.get())
            c.execute("INSERT INTO users (user_type, name, email, password, location) VALUES (?, ?, ?, ?, ?)",
                      (self.user_type.get(), self.name.get(), self.email.get(), hashed_password, self.location.get()))
            user_id = c.lastrowid
            if self.user_type.get() == "Skill Holder":
                c.execute("INSERT INTO skill_holders (user_id, category, skills, contact_number) VALUES (?, ?, ?, ?)",
                          (user_id, self.category.get(), self.skills.get(), self.contact_number.get()))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.window.destroy()
            if self.user_type.get() == "Skill Holder":
                SkillHolderDashboard(self.window.master, user_id)
            else:
                CustomerDashboard(self.window.master, user_id)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists")
        finally:
            conn.close()
