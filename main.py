# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/13
# @Time : 11:57
import hashlib
import random
from sqlalchemy import func
from database import SessionLocal, Transaction
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

    # Hash the password using SHA-256 for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Generate a new account number
    account_number = generate_account_number()

    # Create a new User instance
    new_user = User(
        firstname=firstname,
        lastname=lastname,
        gender=gender,
        phone_number=phone_number,
        email=email,
        password=hashed_password,
        account_number=account_number  # Add account number to the User instance
    )

    # Save the new user to the database
    with SessionLocal() as session:
        session.add(new_user)
        session.commit()

    print("User registration successful!")

    # Call banking_operations after successful registration
    banking_operations(account_number, new_user)


def login_user():
    # Get user input for login
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Query the database for the user
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == username).first()

    if user and user.verify_password(password):
        print("Login successful!")
        return user
    else:
        print("Login failed. Username or password is incorrect.")
        return None


# Function to perform banking operations for a logged-in user
def banking_operations(account, user, account_number):
    username = user.username.upper()
    print(f"\nWelcome, {username}! Your account balance: ${view_balance}")
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
            view_balance(account_number)
        elif choice == "5":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")


# Function to make Deposit
def make_deposit(account_number, user):
    amount = float(input("Enter the deposit amount: "))

    # Create a new Transaction instance for the deposit
    deposit_transaction = Transaction(
        account_number=account_number,
        firstName=user.firstname,
        lastName=user.lastname,
        deposits=amount,
        withdrawals=0.0  # Since it's a deposit, set withdrawals to 0
    )

    # Save the deposit transaction to the database
    with SessionLocal() as session:
        session.add(deposit_transaction)
        session.commit()

    print(f"Deposit of ${amount} successful.")

# Function to make Withdrawal
def make_withdrawal(account_number, user):
    amount = float(input("Enter the withdrawal amount: "))

    # Create a new Transaction instance for the withdrawal
    withdrawal_transaction = Transaction(
        account_number=account_number,
        firstName=user.firstname,
        lastName=user.lastname,
        deposits=0.0,  # Since it's a withdrawal, set deposits to 0
        withdrawals=amount
    )

    # Save the withdrawal transaction to the database
    with SessionLocal() as session:
        session.add(withdrawal_transaction)
        session.commit()

    print(f"Withdrawal of ${amount} successful.")


# Function to get a user's current balance from the transaction log
def view_balance(account_number):
    # Query the transactions table to get the current balance for the account
    with SessionLocal() as session:
        # Calculate the total deposits and withdrawals for the account
        total_deposits = session.query(func.sum(Transaction.deposits)).filter_by(account_number=account_number).scalar() or 0.0
        total_withdrawals = session.query(func.sum(Transaction.withdrawals)).filter_by(account_number=account_number).scalar() or 0.0

        # Calculate the current balance
        current_balance = total_deposits - total_withdrawals

        print(f"Account balance: ${current_balance}")


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
            logged_in_user = login_user()
            if logged_in_user:
                # Continue with banking operations for the logged-in user
                account_number = logged_in_user.account_number
                account = Account(logged_in_user)  # Assuming you have an Account class
                account.account_number = account_number
                banking_operations(account, logged_in_user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
