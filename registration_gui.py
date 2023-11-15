# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/14
# @Time : 09:28

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import random
import hashlib
from database import SessionLocal, User
from sqlalchemy.exc import IntegrityError
from login_gui import LoginApp


class RegistrationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("User Registration")
        self.master.geometry("800x800")

        # Use Ubuntu font
        ubuntu_font = tkfont.Font(family="Ubuntu", size=12)

        # Update label and entry styles
        label_style = {'font': ubuntu_font}
        entry_style = {'font': ubuntu_font, 'width': 30}

        # Labels and entries
        self.label_first_name = tk.Label(master, text="First Name:", **label_style)
        self.label_first_name.pack(pady=10)

        self.entry_first_name = tk.Entry(master, **entry_style)
        self.entry_first_name.pack(pady=10)

        self.label_last_name = tk.Label(master, text="Last Name:", **label_style)
        self.label_last_name.pack(pady=10)

        self.entry_last_name = tk.Entry(master, **entry_style)
        self.entry_last_name.pack(pady=10)

        self.label_gender = tk.Label(master, text="Gender:", **label_style)
        self.label_gender.pack(pady=10)

        # Use a larger font for OptionMenu
        gender_font = tkfont.Font(family="Ubuntu", size=13)
        ttk.Style().configure('TMenubutton', font=gender_font)

        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")  # Default value
        gender_options = ["Male", "Female"]
        self.gender_menu = ttk.OptionMenu(master, self.gender_var, *gender_options)
        self.gender_menu.pack(pady=10)

        self.label_phone_number = tk.Label(master, text="Phone Number:", **label_style)
        self.label_phone_number.pack(pady=10)

        self.entry_phone_number = tk.Entry(master, **entry_style)
        self.entry_phone_number.pack(pady=10)

        self.label_email = tk.Label(master, text="Email:", **label_style)
        self.label_email.pack(pady=10)

        self.entry_email = tk.Entry(master, **entry_style)
        self.entry_email.pack(pady=10)

        # Password generation checkbox
        self.use_generated_password = tk.BooleanVar()
        self.use_generated_password.set(False)  # Default value

        self.checkbox_generate_password = tk.Checkbutton(master, text="Generate Strong Password",
                                                         variable=self.use_generated_password,
                                                         command=self.toggle_password_entry, **label_style)
        self.checkbox_generate_password.pack(pady=10)

        self.label_password = tk.Label(master, text="Password:", **label_style)
        self.label_password.pack(pady=10)

        self.entry_password = tk.Entry(master, show="*", **entry_style)
        self.entry_password.pack(pady=10)

        self.label_password_confirmation = tk.Label(master, text="Confirm Password:", **label_style)
        self.label_password_confirmation.pack(pady=10)

        self.entry_password_confirmation = tk.Entry(master, show="*", **entry_style)
        self.entry_password_confirmation.pack(pady=10)

        # Style for the register button
        btn_style = {'font': ubuntu_font, 'background': '#3498db', 'foreground': 'white', 'width': 15, 'pady': 5}

        # Register button
        self.btn_register = tk.Button(master, text="Register", command=self.register_user, **btn_style)
        self.btn_register.pack(pady=10)

    @staticmethod
    def generate_account_number():
        return random.randint(100000, 999999)

    def toggle_password_entry(self):
        # Enable or disable the password entry based on the checkbox state
        state = tk.NORMAL if not self.use_generated_password.get() else tk.DISABLED
        self.entry_password.configure(state=state)
        self.entry_password_confirmation.configure(state=state)

    def register_user(self):
        first_name = self.entry_first_name.get().strip()
        last_name = self.entry_last_name.get()
        gender = self.gender_var.get()
        phone_number = self.entry_phone_number.get()
        email = self.entry_email.get()
        password_confirmation = self.entry_password_confirmation.get()

        if self.use_generated_password.get():
            password = self.generate_strong_password()
            # Display the generated password in a pop-up dialog
            messagebox.showinfo("Generated Password", f"Your generated password is:\n{password}")
        else:
            password = self.entry_password.get()

        if not self.use_generated_password.get() and password != password_confirmation:
            messagebox.showerror("Error", "Passwords do not match. Registration failed.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            account_number = self.generate_account_number()

            # Create a new User instance
            new_user = User(
                account_number=account_number,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                phone_number=phone_number,
                email=email,
                password=hashed_password,
                password_confirmation=hashed_password
            )

            # Save the new user to the database
            with SessionLocal() as session:
                session.add(new_user)
                session.commit()

            messagebox.showinfo("Success", "User registration successful!")
        except IntegrityError:
            messagebox.showerror("Error", "This username or email is already taken. Please choose a different one.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during registration: {e}")

        self.master.destroy()  # Close the registration window
        login_window = tk.Tk()
        login_app = LoginApp(login_window)
        login_window.mainloop()

    @staticmethod
    def generate_strong_password():
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=<>?/"
        password_length = 15
        generated_password = ''.join(random.choice(characters) for i in range(password_length))
        return generated_password


if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()
