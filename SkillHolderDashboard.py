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
class SkillHolderDashboard:
    def __init__(self, master, user_id):
        self.window = tk.Toplevel(master)
        self.window.title("Skill Holder Dashboard")
        self.window.geometry("500x600")
        
        self.user_id = user_id
        self.load_user_data()
        
        self.create_welcome_message()
        
        self.profile_frame = tk.Frame(self.window)
        self.profile_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        self.display_profile()
        
        tk.Button(self.window, text="Edit Profile", command=self.edit_profile).pack(pady=10)
    
    def load_user_data(self):
        conn = sqlite3.connect('hac.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (self.user_id,))
        self.user = c.fetchone()
        c.execute("SELECT * FROM skill_holders WHERE user_id=?", (self.user_id,))
        self.skill_holder = c.fetchone()
        conn.close()
    
    def create_welcome_message(self):
        welcome_frame = tk.Frame(self.window)
        welcome_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(welcome_frame, text=f"Welcome, {self.user[2]}!", font=("Helvetica", 16, "bold")).pack(anchor="w")
        tk.Label(welcome_frame, text="Your profile has been created with the following details:", font=("Helvetica", 12)).pack(anchor="w", pady=(5, 10))
        
        details = [
            f"Name: {self.user[2]}",
            f"Email: {self.user[3]}",
            f"Location: {self.user[5]}",
            f"Category: {self.skill_holder[2]}",
            f"Skills: {self.skill_holder[3]}",
            f"Contact Number: {self.skill_holder[4]}"
        ]
        
        for detail in details:
            tk.Label(welcome_frame, text=detail, font=("Helvetica", 10)).pack(anchor="w", pady=2)
        
        tk.Label(welcome_frame, text="Your profile is now visible to customers in your area.", font=("Helvetica", 12, "italic")).pack(anchor="w", pady=(10, 0))
    
    def display_profile(self):
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.profile_frame, text="Your Profile", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        details = [
            ("Name", self.user[2]),
            ("Email", self.user[3]),
            ("Location", self.user[5]),
            ("Category", self.skill_holder[2]),
            ("Skills", self.skill_holder[3]),
            ("Contact Number", self.skill_holder[4])
        ]
        
        for label, value in details:
            frame = tk.Frame(self.profile_frame)
            frame.pack(fill=tk.X, pady=5)
            tk.Label(frame, text=f"{label}:", width=15, anchor="e").pack(side=tk.LEFT, padx=(0, 10))
            tk.Label(frame, text=value, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def edit_profile(self):
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Edit Profile")
        edit_window.geometry("400x400")
        
        tk.Label(edit_window, text="Edit Your Profile", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        name_var = tk.StringVar(value=self.user[2])
        location_var = tk.StringVar(value=self.user[5])
        category_var = tk.StringVar(value=self.skill_holder[2])
        skills_var = tk.StringVar(value=self.skill_holder[3])
        contact_var = tk.StringVar(value=self.skill_holder[4])
        
        fields = [
            ("Name", name_var),
            ("Location", location_var),
            ("Category", category_var),
            ("Skills", skills_var),
            ("Contact Number", contact_var)
        ]
        
        for label, var in fields:
            frame = tk.Frame(edit_window)
            frame.pack(fill=tk.X, pady=5, padx=20)
            tk.Label(frame, text=f"{label}:", width=15, anchor="e").pack(side=tk.LEFT, padx=(0, 10))
            if label == "Category":
                ttk.Combobox(frame, textvariable=var, values=["Tutor", "Photographer", "House Broker"]).pack(side=tk.LEFT, fill=tk.X, expand=True)
            else:
                tk.Entry(frame, textvariable=var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        def save_changes():
            conn = sqlite3.connect('hac.db')
            c = conn.cursor()
            c.execute("UPDATE users SET name=?, location=? WHERE id=?",
                      (name_var.get(), location_var.get(), self.user_id))
            c.execute("UPDATE skill_holders SET category=?, skills=?, contact_number=? WHERE user_id=?",
                      (category_var.get(), skills_var.get(), contact_var.get(), self.user_id))
            conn.commit()
            conn.close()
            
            self.load_user_data()
            self.create_welcome_message()
            self.display_profile()
            edit_window.destroy()
            messagebox.showinfo("Success", "Profile updated successfully!")
        
        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = HACAPP(root)
    root.mainloop()