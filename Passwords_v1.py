import tkinter as tk
from tkinter import messagebox
import sqlite3
import secrets

class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")

        # Create labels and entries for email and password
        self.create_email_password_widgets()

        # Create buttons for generating, saving, updating, and deleting passwords
        self.create_action_buttons()

        # Create listbox to display passwords
        self.create_password_listbox()

        # Connect to the database and load existing passwords
        self.connect_and_load_passwords()

    def create_email_password_widgets(self):
        # Email label and entry
        self.email_label = tk.Label(self.master, text="Email/Username:")
        self.email_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(self.master, width=30)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Password label, entry, and generate button
        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(self.master, width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.generate_button = tk.Button(self.master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

    def create_action_buttons(self):
        # Save, Update, and Delete buttons
        self.save_button = tk.Button(self.master, text="Save", command=self.save_password, bg="#2fc22f")
        self.save_button.grid(row=2, column=0, padx=10, pady=5)
        self.update_button = tk.Button(self.master, text="Update", command=self.update_password)
        self.update_button.grid(row=2, column=1, padx=10, pady=5)
        self.delete_button = tk.Button(self.master, text="Delete", command=self.delete_password, bg="#f50035")
        self.delete_button.grid(row=2, column=2, padx=10, pady=5)

    def create_password_listbox(self):
        # Listbox to display passwords
        self.password_listbox = tk.Listbox(self.master, width=50)
        self.password_listbox.grid(row=3, columnspan=3, padx=10, pady=5)

    def connect_and_load_passwords(self):
        # Connect to the database and load existing passwords
        self.connection = sqlite3.connect("passwords.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                              (email TEXT PRIMARY KEY, password TEXT)''')
        self.load_passwords()

    def generate_password(self):
        # Generate a random password
        password = ''.join(secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_") for i in range(25))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def save_password(self):
        # Save the email and password to the database
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email and password:
            try:
                self.cursor.execute("INSERT INTO passwords (email, password) VALUES (?, ?)", (email, password))
                self.connection.commit()
                self.password_listbox.insert(tk.END, email)
                messagebox.showinfo("Success", "Password saved successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Email already exists!")
        else:
            messagebox.showerror("Error", "Email and password cannot be empty!")

    def update_password(self):
        # Update the password in the database
        selected_index = self.password_listbox.curselection()
        if selected_index:
            selected_email = self.password_listbox.get(selected_index)
            new_password = self.password_entry.get()
            if new_password:
                self.cursor.execute("UPDATE passwords SET password=? WHERE email=?", (new_password, selected_email))
                self.connection.commit()
                messagebox.showinfo("Success", "Password updated successfully!")
            else:
                messagebox.showerror("Error", "Password cannot be empty!")
        else:
            messagebox.showerror("Error", "No item selected!")

    def delete_password(self):
        # Delete the password from the database
        selected_index = self.password_listbox.curselection()
        if selected_index:
            selected_email = self.password_listbox.get(selected_index)
            self.cursor.execute("DELETE FROM passwords WHERE email=?", (selected_email,))
            self.connection.commit()
            self.password_listbox.delete(selected_index)
            messagebox.showinfo("Success", "Password deleted successfully!")
        else:
            messagebox.showerror("Error", "No item selected!")

    def load_passwords(self):
        # Load passwords from the database
        self.cursor.execute("SELECT email FROM passwords")
        emails = self.cursor.fetchall()
        for email in emails:
            self.password_listbox.insert(tk.END, email[0])

    def copy_password(self):
        # Copy the selected password to the clipboard
        selected_index = self.password_listbox.curselection()
        if selected_index:
            selected_email = self.password_listbox.get(selected_index)
            self.cursor.execute("SELECT password FROM passwords WHERE email=?", (selected_email,))
            password = self.cursor.fetchone()
            if password:
                password = password[0]
                self.master.clipboard_clear()
                self.master.clipboard_append(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
            else:
                messagebox.showerror("Error", "Failed to retrieve password!")
        else:
            messagebox.showerror("Error", "No item selected!")

    def copy_email(self):
        # Copy the selected email to the clipboard
        selected_index = self.password_listbox.curselection()
        if selected_index:
            selected_email = self.password_listbox.get(selected_index)
            self.master.clipboard_clear()
            self.master.clipboard_append(selected_email)
            messagebox.showinfo("Success", "Email copied to clipboard!")
        else:
            messagebox.showerror("Error", "No item selected!")


root = tk.Tk()
app = PasswordManager(root)
root.mainloop()
