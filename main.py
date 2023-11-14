# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/13
# @Time : 11:57

# main.py

import tkinter as tk
from tkinter import ttk
from login_gui import LoginApp
from banking_gui import BankingGUI

from registration_gui import RegistrationApp


class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Banking App")
        self.master.geometry("400x300")  # Set the initial window size

        # Style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=(10, 5), font=('Ubuntu', 12))

        # Buttons
        self.btn_register = ttk.Button(master, text="Register", command=self.show_registration)
        self.btn_register.pack(pady=20)

        self.btn_login = ttk.Button(master, text="Login", command=self.show_login)
        self.btn_login.pack(pady=20)

    def show_registration(self):
        registration_window = tk.Toplevel(self.master)
        registration_app = RegistrationApp(registration_window)
        registration_window.wait_window()  # Wait for the registration window to be closed
        if registration_app.user:
            self.show_banking(registration_app.user)

    def show_login(self):
        login_window = tk.Toplevel(self.master)
        login_app = LoginApp(login_window)
        login_window.wait_window()  # Wait for the login window to be closed
        if login_app.user:
            self.show_banking(login_app.user)

    def show_banking(self, user):
        banking_window = tk.Toplevel(self.master)
        banking_app = BankingGUI(banking_window, user.account_number)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
