# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/14
# @Time : 09:53

import tkinter as tk
from tkinter import messagebox
import hashlib

from sqlalchemy.orm import sessionmaker

from banking_gui import BankingGUI
from database import SessionLocal, User, engine
from sqlalchemy.exc import NoResultFound


class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("User Login")

        self.label_username = tk.Label(master, text="Username:")
        self.label_username.pack()

        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="Password:")
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack()

        self.btn_login = tk.Button(master, text="Login", command=self.login_user)
        self.btn_login.pack()

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
