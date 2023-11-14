# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/14
# @Time : 09:53

import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import hashlib

from sqlalchemy.orm import sessionmaker

from banking_gui import BankingGUI
from database import SessionLocal, User, engine
from sqlalchemy.exc import NoResultFound


class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("User Login")

        # Use Ubuntu font
        ubuntu_font = tkfont.Font(family="Ubuntu", size=12)

        # Update label and entry styles
        label_style = {'font': ubuntu_font}
        entry_style = {'font': ubuntu_font, 'width': 30}

        self.label_username = tk.Label(master, text="Username:", **label_style)
        self.label_username.pack(pady=10)

        self.entry_username = tk.Entry(master, **entry_style)
        self.entry_username.pack(pady=10)

        self.label_password = tk.Label(master, text="Password:", **label_style)
        self.label_password.pack(pady=10)

        self.entry_password = tk.Entry(master, show="*", **entry_style)
        self.entry_password.pack(pady=10)

        # Style for the login button
        btn_style = {'font': ubuntu_font, 'background': '#3498db', 'foreground': 'white', 'width': 15, 'pady': 10}

        self.btn_login = tk.Button(master, text="Login", command=self.login_user, **btn_style)
        self.btn_login.pack(pady=10)

    def login_user(self):
        first_name = self.entry_username.get().strip()
        password = self.entry_password.get()

        Session = sessionmaker(bind=engine)
        session = Session()

        print(f"Username: {first_name}, Password: {password}")

        try:
            first_name = first_name.strip()
            # Query the database for the user
            with SessionLocal() as session:
                user = session.query(User).filter(User.first_name == first_name).first()

            print(f"User: {user}")

            # Verify the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if user.password == hashed_password:
                print("Password verification successful")
                messagebox.showinfo("Login Successful", "Welcome back, {}".format(first_name))
                self.open_banking_gui(user)
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password")
        except NoResultFound:
            messagebox.showerror("Login Failed", "Incorrect username or password")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during login: {e}")
        finally:
            session.close()

    def open_banking_gui(self, user):
        self.master.destroy()
        banking_window = tk.Tk()
        banking_gui = BankingGUI(banking_window, account_number=user.account_number)
        banking_window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()
