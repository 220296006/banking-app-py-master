import secrets
import tkinter as tk
import tkinter.font as tkfont
import random
import hashlib
import re
from database import SessionLocal, User
from sqlalchemy.exc import IntegrityError
from login_gui import LoginApp
from tkinter import ttk, messagebox


class RegistrationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("User Registration")
        self.master.geometry("800x800")
        self.generated_password = ""

        ubuntu_font = tkfont.Font(family="Ubuntu", size=12)
        label_style = {'font': ubuntu_font}
        entry_style = {'font': ubuntu_font, 'width': 30}
        btn_style = {'font': ubuntu_font, 'background': '#3498db', 'foreground': 'white', 'width': 15, 'pady': 5}

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

        gender_font = tkfont.Font(family="Ubuntu", size=13)
        ttk.Style().configure('TMenubutton', font=gender_font)

        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
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

        self.use_generated_password = tk.BooleanVar()
        self.use_generated_password.set(False)

        self.checkbox_generate_password = tk.Checkbutton(master, text="Generate Strong Password",
                                                         variable=self.use_generated_password,
                                                         command=self.toggle_password_entry, **label_style)
        self.checkbox_generate_password.pack(pady=10)

        self.label_generated_password = tk.Label(master, text="", **label_style)
        self.label_generated_password.pack(pady=5)

        self.label_password = tk.Label(master, text="Password:", **label_style)
        self.label_password.pack(pady=10)

        self.entry_password = tk.Entry(master, show="*", **entry_style)
        self.entry_password.pack(pady=10)

        self.show_password_var = tk.BooleanVar()
        self.show_password_var.set(False)

        self.checkbox_show_password = tk.Checkbutton(master, text="Show Password",
                                                     variable=self.show_password_var,
                                                     command=self.toggle_password_visibility, **label_style)
        self.checkbox_show_password.pack(pady=10)

        self.label_password_confirmation = tk.Label(master, text="Confirm Password:", **label_style)
        self.label_password_confirmation.pack(pady=10)

        self.entry_password_confirmation = tk.Entry(master, show="*", **entry_style)
        self.entry_password_confirmation.pack(pady=10)

        self.label_password_strength = tk.Label(master, text="", **label_style)
        self.label_password_strength.pack(pady=5)

        self.entry_phone_number.bind("<FocusOut>", self.validate_phone_number)
        self.entry_email.bind("<FocusOut>", self.validate_email)
        self.entry_password.bind("<KeyRelease>", self.on_password_change)

        self.btn_register = tk.Button(master, text="Register", command=self.register_user, **btn_style)
        self.btn_register.pack(pady=10)

    def toggle_password_entry(self):
        state = tk.NORMAL if not self.use_generated_password.get() else tk.DISABLED
        self.entry_password.configure(state=state)
        self.entry_password_confirmation.configure(state=state)

        if self.use_generated_password.get():
            # Generate and store the password
            self.generated_password = self.generate_strong_password(self)
            self.label_generated_password.config(text=f"Generated Password: {self.generated_password}")
        else:
            self.label_generated_password.config(text="")

    def toggle_password_visibility(self):
        show_password = self.show_password_var.get()
        show_char = "" if show_password else "*"
        self.entry_password.configure(show=show_char)
        self.entry_password_confirmation.configure(show=show_char)

    def validate_phone_number(self, event):
        phone_number = self.entry_phone_number.get()
        if not (phone_number.isdigit() and len(phone_number) == 10):
            messagebox.showerror("Error", "Please enter a valid 10-digit phone number.")
            self.entry_phone_number.delete(0, tk.END)

    def validate_email(self, event):
        email = self.entry_email.get()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            self.entry_email.delete(0, tk.END)

    def register_user(self):
        first_name = self.entry_first_name.get().strip()
        last_name = self.entry_last_name.get()
        gender = self.gender_var.get()
        phone_number = self.entry_phone_number.get()
        email = self.entry_email.get()
        password_confirmation = self.entry_password_confirmation.get()

        # Use the stored generated password if checkbox is checked
        if self.use_generated_password.get():
            password = self.generated_password
            messagebox.showinfo("Generated Password", f"Your generated password is:\n{password}")
        else:
            password = self.entry_password.get()

        if not self.use_generated_password.get() and password != password_confirmation:
            messagebox.showerror("Error", "Passwords do not match. Registration failed.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            account_number = self.generate_account_number()
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

            with SessionLocal() as session:
                session.add(new_user)
                session.commit()

            messagebox.showinfo("Success", "User registration successful!")
        except IntegrityError:
            messagebox.showerror("Error", "This username or email is already taken. Please choose a different one.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during registration: {e}")

        self.master.destroy()
        login_window = tk.Tk()
        login_app = LoginApp(login_window)
        login_window.mainloop()

    @staticmethod
    def generate_account_number():
        return random.randint(100000, 999999)

    @staticmethod
    def generate_strong_password(self):
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=<>?/"
        password_length = secrets.choice(range(5, 16))
        generated_password = ''.join(random.choice(characters) for i in range(password_length))

        # Update the password entry with the generated password
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, generated_password)

        return generated_password

    def check_password_match(self):
        password = self.entry_password.get()
        confirm_password = self.entry_password_confirmation.get()

        if password == confirm_password:
            self.label_password_strength.config(text="Password Match", fg="green")
        else:
            self.label_password_strength.config(text="Password Mismatch", fg="red")

    @staticmethod
    def password_strength(password):
        # Criteria for password strength
        length_criteria = len(password) >= 8
        digit_criteria = re.search(r"\d", password) is not None
        lowercase_criteria = re.search(r"[a-z]", password) is not None
        uppercase_criteria = re.search(r"[A-Z]", password) is not None
        special_char_criteria = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None

        # Check overall strength
        if length_criteria and digit_criteria and lowercase_criteria and uppercase_criteria and special_char_criteria:
            return "Strong", "green"
        elif length_criteria and digit_criteria and lowercase_criteria and uppercase_criteria:
            return "Medium", "orange"
        else:
            return "Weak", "red"

    def on_password_change(self, *args):
        password = self.entry_password.get()
        strength, color = self.password_strength(password)
        self.label_password_strength.config(text=f" {strength} Password", fg=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()
