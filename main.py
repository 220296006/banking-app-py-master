# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/13
# @Time : 11:57

import hashlib
import random

from database import SessionLocal
from models import User, Account


# Function to generate a unique account number
def generate_account_number():
    # Generate a random account number (you can use a more sophisticated approach)
    return random.randint(100000, 999999)


# Function to register a new user
def register_user():
    # Get user input for registration
    firstname = input("Enter your first name: ")
    lastname = input("Enter your last name: ")
    gender = input("Enter your gender: ")
    phone_number = input("Enter your phone number: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    password_confirmation = input("Confirm your password: ")

    # Check if passwords match
    if password != password_confirmation:
        print("Passwords do not match. Registration failed.")
        return

    # Generate a new account number
    account_number = generate_account_number()

    # Create a new User instance
    new_user = User(
        account_number=account_number,
        firstname=firstname,
        lastname=lastname,
        gender=gender,
        phone_number=phone_number,
        email=email,
        password=password
    )

    # Save the new user to the database
    with SessionLocal() as session:
        session.add(new_user)
        session.commit()

    print("User registration successful!")

    # Call banking_operations after successful registration
    banking_operations(account, user, account_number)


# Function to log in a user
def login_user():
    # Get user input for username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Hash the input password
    hashed_input_password = hashlib.sha256(password.encode()).hexdigest()

    # Check if the user exists in bank_users.txt
    with open("bank_users.txt", "r") as file:
        lines = file.readlines()
        user_found = False
        account_number = None
        user = None
        for i in range(0, len(lines), 4):
            stored_username = lines[i + 1].strip().split(": ")[1]
            stored_password = lines[i + 2].strip().split(": ")[1]
            if username == stored_username and hashed_input_password == stored_password:
                user_found = True
                account_number = int(lines[i].strip().split(": ")[1])
                user = User(stored_username, hashed_input_password)  # Create a User instance
                break

        if user_found:
            print("Login successful!")

            # Create a new Account instance for the logged-in user
            account = Account(user)
            account.account_number = account_number

            # Get and display the user's current balance
            return account_number, user
        else:
            print("Login failed. Username or password is incorrect.")
            return None, None


# Function to perform banking operations for a logged-in user
def banking_operations(account, user, account_number):
    username = user.username.upper()
    current_balance = get_current_balance(account_number)
    print(f"\nWelcome, {username}! Your account balance: ${current_balance}")
    while True:
        print("\nBanking Options:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Invest")
        print("4. View Balance")
        print("5. Log out")
        choice = input("Enter your choice: ")

        if choice == "1":
            make_deposit(account, user)
        elif choice == "2":
            make_withdrawal(account, user)
        elif choice == "3":
            # Implement the logic to handle investments
            pass
        elif choice == "4":
            current_balance = get_current_balance(account.account_number)
            print(f"Account balance: ${current_balance}")
        elif choice == "5":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")


# Function to make Deposit
def make_deposit(account, user):
    amount = float(input("Enter the deposit amount: "))

    if amount > 0:  # Check if the deposit amount is positive
        if account.deposit(amount):
            print(f"Deposit of ${amount} successful.")

            # Access the username attribute from the user object and convert it to uppercase
            username = user.username.upper()

            # Get the current balance after the deposit
            current_balance = account.view_balance()

            # Save the deposit information to transaction_log.txt
            with open("transaction_log.txt", "a") as log_file:
                log_file.write("## Deposits ##\n")
                log_file.write(f"Username: {username}\n")
                log_file.write(f"Account Number: {account.account_number}\n")
                log_file.write(f"Amount: ${amount}\n")
                log_file.write(f"Current Balance: ${current_balance}\n")
                log_file.write("#############\n")
        else:
            print("Invalid deposit amount.")
    else:
        print("Invalid deposit amount. Please enter an amount greater than zero.")


# Function to make Withdrawal
def make_withdrawal(account, user):
    amount = float(input("Enter the withdrawal amount: "))
    if account.withdraw(amount):
        print(f"Withdrawal of ${amount} successful.")

        # Access the username attribute from the user object and convert it to uppercase
        username = user.username.upper()

        # Get the current balance after the withdrawal
        current_balance = account.view_balance()

        # Save the withdrawal information to transaction_log.txt
        with open("transaction_log.txt", "a") as log_file:
            log_file.write("## Withdrawals ##\n")
            log_file.write(f"Username: {username}\n")
            log_file.write(f"Account Number: {account.account_number}\n")
            log_file.write(f"Amount: ${amount}\n")
            log_file.write(f"Current Balance: ${current_balance}\n")
            log_file.write("#################\n")
    else:
        print("Invalid withdrawal amount or insufficient balance.")


# Function to get a user's current balance from the transaction log
def get_current_balance(account_number):
    with open("transaction_log.txt", "r") as log_file:
        lines = log_file.readlines()
        current_balance = 0  # Initialize with zero

        in_user_transactions = False
        for line in lines:
            if in_user_transactions:
                if line.startswith("Username:"):
                    # Reached the end of user transactions
                    break
                elif line.startswith("Amount: $"):
                    amount = float(line.split("$")[1].strip())
                    if "Withdrawals" in line:
                        current_balance -= amount  # Subtract withdrawal amount
                    else:
                        current_balance += amount  # Add deposit amount
            if f"Account Number: {account_number}" in line:
                in_user_transactions = True

    return current_balance


if __name__ == "__main__":
    account = None  # Initialize account

    while True:
        print("\nWelcome to the Banking App")
        print("1. Register a new user")
        print("2. Log in")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            account_number, user = login_user()
            if account_number:
                account = Account(user)  # Create a new account
                account.account_number = account_number
                banking_operations(account, user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
