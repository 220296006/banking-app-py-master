import tkinter as tk
from tkinter import ttk
from login_gui import LoginApp
from banking_gui import BankingGUI
from registration_gui import RegistrationApp


class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Banking App")
        self.master.geometry("600x600")
        self.master.configure(bg='gray')

        logo_image = tk.PhotoImage(file='Fast Money.png')
        self.label_logo = tk.Label(master, image=logo_image, width=300, height=400)
        self.label_logo.image = logo_image
        self.label_logo.pack(pady=20)

        self.label_welcome = tk.Label(master, text="Welcome to VP Bank", font=("Helvetica", 24))
        self.label_welcome.pack(pady=20)

        self.style = ttk.Style()
        self.style.configure("TButton", padding=(10, 5), font=('Ubuntu', 12))

        self.btn_register = ttk.Button(master, text="Register", command=self.show_registration)
        self.btn_register.pack(pady=20)

        self.btn_login = ttk.Button(master, text="Login", command=self.show_login)
        self.btn_login.pack(pady=20)

        self.btn_exit = tk.Button(master, text="Exit", command=self.exit_system, width=20, height=2)
        self.btn_exit.pack(pady=20)

    def exit_system(self):
        self.master.destroy()

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
