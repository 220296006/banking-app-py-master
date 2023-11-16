import hashlib
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import random
import secrets
from database import SessionLocal, User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ForgotPasswordGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Forgot Password")
        self.master.geometry("400x300")
        self.master.configure(bg='gray')

        ubuntu_font = tkfont.Font(family="Ubuntu", size=12)
        label_style = {'font': ubuntu_font}
        entry_style = {'font': ubuntu_font, 'width': 30}
        btn_style = {'font': ubuntu_font, 'background': '#3498db', 'foreground': 'white', 'width': 15, 'pady': 5}

        # Labels
        self.label_email = tk.Label(master, text="Email:", **label_style)
        self.label_email.pack(pady=10)

        # Entry for email
        self.entry_email = tk.Entry(master, **entry_style)
        self.entry_email.pack(pady=10)

        # Submit button
        self.btn_submit = tk.Button(master, text="Submit", command=self.send_new_password, **btn_style)
        self.btn_submit.pack(pady=10)

        self.btn_exit = tk.Button(master, text="Exit", command=self.exit_system, width=20, height=2)
        self.btn_exit.pack(pady=20)

    def exit_system(self):
        self.master.destroy()

    def send_new_password(self):
        email = self.entry_email.get()

        with SessionLocal() as session:
            try:
                user = session.query(User).filter(User.email == email).one()
            except Exception:
                messagebox.showerror("Error", "No user found with the provided email.")
                return

        # Generate a new password
        new_password = self.generate_strong_password()

        # Update the user's password in the database
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        user.password = hashed_password

        # Send the new password to the user via email
        self.send_email(user.email, new_password)

        # Commit changes to the database
        with SessionLocal() as session:
            session.commit()

        messagebox.showinfo("Success", "A new password has been sent to your email address.")

    @staticmethod
    def generate_strong_password():
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=<>?/"
        password_length = secrets.choice(range(10, 16))
        generated_password = ''.join(random.choice(characters) for _ in range(password_length))
        return generated_password

    @staticmethod
    def send_email(to_email, new_password):
        # Your email and password for sending the email
        from_email = "thabisomatsaba96@gmail.com"
        email_password = " ysjqkbfnhvpnfzwo"

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = "New Password"

        # The body of the email
        body = f"Your new password is: {new_password}"
        message.attach(MIMEText(body, 'plain'))

        # Connect to the server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, email_password)
            server.sendmail(from_email, to_email, message.as_string())


if __name__ == "__main__":
    root = tk.Tk()
    forgot_password_app = ForgotPasswordGUI(root)
    root.mainloop()
