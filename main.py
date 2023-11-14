# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/13
# @Time : 11:57

import hashlib
import random
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from database import SessionLocal, Transaction, User, Investment
from models import Account


# Function to generate a unique account number
def generate_account_number():
    return random.randint(100000, 999999)


# Function to register a new user
def register_user():
    try:
        firstname = input("Enter your first name: ")
        lastname = input("Enter your last name: ")
        gender = input("Enter your gender: ")
        phone_number = input("Enter your phone number: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        password_confirmation = input("Confirm your password: ")

        if password != password_confirmation:
            print("Passwords do not match. Registration failed.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        account_number = generate_account_number()

        # Create a new User instance
        new_user = User(
            account_number=account_number,
            first_name=firstname,
            last_name=lastname,
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

        print("User registration successful!")

        # Call banking_operations after successful registration
        banking_operations(account_number)

    except IntegrityError as e:
        print("Error: This username or email is already taken. Please choose a different one.")

    except Exception as e:
        print(f"An error occurred during registration: {e}")


def login_user():
    try:
        # Get user input for login
        first_name = input("Enter your username: ")
        password = input("Enter your password: ")

        # Query the database for the user
        with SessionLocal() as session:
            user = session.query(User).filter(User.first_name == first_name).first()

        if user and user.verify_password(password):
            print("Login successful!")
            return user
        else:
            print("Login failed. Username or password is incorrect.")
            return None
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return None


# Function to perform banking operations for a logged-in user
def banking_operations(user):
    try:
        # Get the user based on the account number
        with SessionLocal() as session:
            user = session.query(User).filter_by(account_number=account_number).first()

        # Get the initial balance when the user logs in
        initial_balance = view_balance(account_number)
        print(
            f"\nWelcome, {user.first_name.upper()} {user.last_name.upper()}! Your account balance: R{initial_balance}")

        while True:
            print("\nBanking Options:")
            print("1. Transaction")
            print("2. Investment")
            print("3. View Balance")
            print("4. Statement")
            print("5. Log out")
            choice = input("Enter your choice: ")

            if choice == "1":
                transaction_choice = input("Choose transaction type:\n1. Deposit\n2. Withdraw\nEnter your choice: ")
                if transaction_choice == "1":
                    make_deposit(account_number, user)
                elif transaction_choice == "2":
                    make_withdrawal(account_number, user)
                else:
                    print("Invalid transaction choice. Please enter 1 or 2.")
            elif choice == "2":
                investment_choice = input(
                    "Choose investment type:\n1. Calculate Bond/Home Loan\n2. Invest\nEnter your choice: ")
                if investment_choice == "1":
                    calculate_bond_or_home_loan(account_number, user.first_name, user.last_name)
                elif investment_choice == "2":
                    make_investment(account_number, user.first_name, user.last_name)
                else:
                    print("Invalid investment choice. Please enter 1 or 2.")
            elif choice == "3":
                balance = view_balance(account_number)
                print(f"\nYour account balance: R{balance}")
            elif choice == "4":
                # Get and display user statement
                transactions, investments = get_user_statement(account_number)

                print("\nTransaction History:")
                for transaction in transactions:
                    print(
                        f"Date: {transaction.timestamp}, Type: Transaction, Amount: {transaction.deposits - transaction.withdrawals}")

                print("\nInvestment History:")
                for investment in investments:
                    print(
                        f"Date: {investment.timestamp}, Type: Investment, Amount: {investment.bond + investment.investment}")

                current_balance = view_balance(account_number)
                print(f"\nYour current balance: R{current_balance}")
            elif choice == "5":
                print("Logging out.")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

    except Exception as e:
        print(f"An error occurred during banking operations: {e}")


# Function to make Deposit
def make_deposit(account_number, user):
    amount = float(input("Enter the deposit amount: "))

    # Create a new Transaction instance for the deposit
    deposit_transaction = Transaction(
        account_number=account_number,
        first_name=user.first_name,
        last_name=user.last_name,
        deposits=amount,
        withdrawals=0.0  # Since it's a deposit, set withdrawals to 0
    )

    # Save the deposit transaction to the database
    with SessionLocal() as session:
        session.add(deposit_transaction)
        session.commit()

    print(f"Deposit of R{amount} successful.")


# Function to make Withdrawal
def make_withdrawal(account_number, user):
    # Get the user's current balance
    current_balance = view_balance(account_number)

    # Check if the balance is sufficient for withdrawal
    if current_balance <= 0:
        print("Insufficient funds. Withdrawal failed.")
        return

    amount = float(input("Enter the withdrawal amount: "))

    # Check if the withdrawal amount is valid
    if amount <= 0 or amount > current_balance:
        print("Invalid withdrawal amount. Please enter a valid amount.")
        return

    # Create a new Transaction instance for the withdrawal
    withdrawal_transaction = Transaction(
        account_number=account_number,
        first_name=user.first_name,
        last_name=user.last_name,
        deposits=0.0,  # Since it's a withdrawal, set deposits to 0
        withdrawals=amount
    )

    # Save the withdrawal transaction to the database
    with SessionLocal() as session:
        session.add(withdrawal_transaction)
        session.commit()

    print(f"Withdrawal of R{amount} successful.")


# Function to get a user's current balance from the transaction log
def view_balance(account_number):
    with SessionLocal() as session:
        total_deposits = session.query(func.sum(Transaction.deposits)).filter_by(
            account_number=account_number).scalar() or 0.0
        total_withdrawals = session.query(func.sum(Transaction.withdrawals)).filter_by(
            account_number=account_number).scalar() or 0.0

        # Calculate the current balance
        current_balance = total_deposits - total_withdrawals

        print(f"Account balance: R{current_balance}")

        return current_balance  # Add this line to return the current_balance


# Function to calculate bond/home loan and save to investment table
def calculate_bond_or_home_loan(account_number, first_name, last_name):
    # Query the database for the user
    with SessionLocal() as session:
        user = session.query(User).filter(User.first_name == first_name, User.last_name == last_name).first()

    if not user:
        print("User not found.")
        return

    loan_amount = float(input("Enter the loan amount: "))
    annual_interest_rate = float(input("Enter the annual interest rate (%): "))
    years = int(input("Enter the loan term in years: "))
    interest_type = input("Enter interest type (simple or compound): ").lower()

    # Calculate monthly interest rate
    monthly_interest_rate = annual_interest_rate / 100 / 12

    # Calculate the number of monthly payments
    num_payments = years * 12

    # Calculate monthly payment using the loan formula
    if interest_type == "simple":
        # Calculate monthly payment using simple interest formula
        monthly_payment = (loan_amount * (1 + (annual_interest_rate / 100 * years))) / num_payments
    elif interest_type == "compound":
        # Calculate monthly payment using compound interest formula
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    else:
        print("Invalid interest type. Please enter 'simple' or 'compound'.")
        return

    # Create a new Investment instance for the bond/home loan
    bond_or_loan_investment = Investment(
        account_number=account_number,
        first_name=user.first_name,
        last_name=user.last_name,
        bond=loan_amount,
        investment=0.0,  # Since it's a loan, set investment to 0
        loan_amount=loan_amount,
        annual_interest_rate=annual_interest_rate,
        loan_term_years=years,
        interest_type=interest_type,
        monthly_payment=monthly_payment
    )

    # Save the investment to the database
    with SessionLocal() as session:
        session.add(bond_or_loan_investment)
        session.commit()

    print(f"\nBond/Home Loan calculation successful.")
    print(f"Monthly Payment: R{monthly_payment:.2f}")


# Function to make general investment
def make_investment(account_number, first_name, last_name):
    # Query the database for the user
    with SessionLocal() as session:
        user = session.query(User).filter(User.first_name == first_name, User.last_name == last_name).first()

    amount = float(input("Enter the investment amount: "))
    investment_type = input("Enter the investment type: ")

    # Create a new Investment instance for the general investment
    general_investment = Investment(
        account_number=account_number,
        first_name=user.first_name,
        last_name=user.last_name,
        bond=0.0,  # Since it's a general investment, set bond to 0
        investment=amount,
        investment_type=investment_type
    )

    # Save the investment to the database
    with SessionLocal() as session:
        session.add(general_investment)
        session.commit()

    print(f"\nGeneral Investment of R{amount} successful.")


# Function to get a user's statement (transactions and investments)
def get_user_statement(account_number):
    with SessionLocal() as session:
        # Get transactions
        transactions = session.query(Transaction).filter_by(account_number=account_number).all()

        # Get investments
        investments = session.query(Investment).filter_by(account_number=account_number).all()

    return transactions, investments


if __name__ == "__main__":
    account = None  # Initialize account

    while True:
        try:
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
                    account = Account(logged_in_user, account_number)  # Assuming you have an Account class
                    account.account_number = account_number
                    banking_operations(logged_in_user)  # Pass the user object here
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        except Exception as e:
            print(f"An error occurred: {e}")
