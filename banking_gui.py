# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/14
# @Time : 10:10

import tkinter as tk
from tkinter import messagebox, simpledialog, font

from database import SessionLocal, Transaction, get_user_by_account_number, Investment


class BankingGUI:
    def __init__(self, master, account_number):
        self.user = None
        self.current_balance = None
        self.master = master
        self.master.title("Banking App")
        self.load_user_data(account_number)
        self.master.geometry("600x600")

        # Use Ubuntu font
        ubuntu_font = font.Font(family="Ubuntu", size=16)

        # Update label styles
        label_style = {'font': ubuntu_font, 'padx': 10, 'pady': 10}

        # Welcome message
        if self.user:
            self.label_welcome = tk.Label(master, text=f"Welcome {self.user.first_name} {self.user.last_name}!")
            self.label_welcome.pack(pady=10)

            # Account balance
            self.label_balance = tk.Label(master, text=f"Your Account Balance is: R{self.current_balance:.2f}")
            self.label_balance.pack(pady=10)

            # Buttons
            self.btn_transaction = tk.Button(master, text="Transaction", command=self.show_transaction_options)
            self.btn_transaction.pack(pady=10)

            self.btn_investment = tk.Button(master, text="Investment", command=self.show_investment_options)
            self.btn_investment.pack(pady=10)

            self.btn_statement = tk.Button(master, text="Statement", command=self.view_statement)
            self.btn_statement.pack(pady=10)

            self.btn_view_balance = tk.Button(master, text="View Balance", command=self.view_balance)
            self.btn_view_balance.pack(pady=10)
        else:
            messagebox.showerror("Error", "User not found. Unable to load data.")

    def load_user_data(self, account_number):
        # Query the database to get the user's available balance
        with SessionLocal() as session:
            self.user = get_user_by_account_number(session, account_number)

            if self.user:
                transactions = session.query(Transaction).filter_by(account_number=account_number).all()
                self.current_balance = sum(
                    transaction.deposits - transaction.withdrawals for transaction in transactions)

    def show_transaction_options(self):
        options = "Choose an option:\n1. Deposit\n2. Withdrawal"
        choice = simpledialog.askinteger("Transaction Options", options, minvalue=1, maxvalue=2)
        self.master.geometry("400x400")

        if choice == 1:
            self.perform_deposit()
        elif choice == 2:
            self.perform_withdrawal()

    def perform_deposit(self):
        deposit_amount = simpledialog.askfloat("Deposit", "Enter deposit amount:")
        if deposit_amount:
            self.update_transaction_log(deposit_amount, 0)
            self.master.geometry("400x400")

    def perform_withdrawal(self):
        withdrawal_amount = simpledialog.askfloat("Withdrawal", "Enter withdrawal amount:")
        if withdrawal_amount:
            self.update_transaction_log(0, withdrawal_amount)
            self.master.geometry("400x400")

    def update_transaction_log(self, deposit, withdrawal):
        with SessionLocal() as session:
            new_transaction = Transaction(
                account_number=self.user.account_number,
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                deposits=deposit,
                withdrawals=withdrawal
            )
            session.add(new_transaction)
            session.commit()

            self.load_user_data(self.user.account_number)
            self.label_balance.config(text=f"Your Account Balance is: R{self.current_balance:.2f}")
            self.master.geometry("400x400")

    def show_investment_options(self):
        # Implement the logic to show bond/home loan and invest calculators
        options = "Choose an option:\n1. Bond/Home Loan\n2. Invest Calculators"
        choice = simpledialog.askinteger("Investment Options", options, minvalue=1, maxvalue=2)
        self.master.geometry("400x400")

        if choice == 1:
            self.perform_bond_loan_calculation()
        elif choice == 2:
            self.perform_investment_calculation()

    def perform_bond_loan_calculation(self):
        loan_amount = simpledialog.askfloat("Bond/Home Loan", "Enter loan amount:")
        interest_rate = simpledialog.askfloat("Bond/Home Loan", "Enter annual interest rate:")
        loan_term_years = simpledialog.askinteger("Bond/Home Loan", "Enter loan term (in years):")
        self.master.geometry("400x400")

        if loan_amount and interest_rate and loan_term_years:
            interest_type = simpledialog.askstring("Interest Type", "Enter interest type (simple/compound):")
            if interest_type and interest_type.lower() in ["simple", "compound"]:
                monthly_payment = self.calculate_monthly_payment(loan_amount, interest_rate, loan_term_years,
                                                                 interest_type)
                self.save_investment_details("Bond/Home Loan", loan_amount, interest_rate, loan_term_years,
                                             monthly_payment)
            else:
                messagebox.showerror("Error", "Invalid interest type. Please enter 'simple' or 'compound'.")

    def perform_investment_calculation(self):
        investment_amount = simpledialog.askfloat("Investment", "Enter investment amount:")
        annual_return_rate = simpledialog.askfloat("Investment", "Enter annual return rate:")
        investment_term_years = simpledialog.askinteger("Investment", "Enter investment term (in years):")
        self.master.geometry("400x400")

        if investment_amount and annual_return_rate and investment_term_years:
            future_value = self.calculate_future_value(investment_amount, annual_return_rate, investment_term_years)
            self.save_investment_details("Investment", investment_amount, annual_return_rate, investment_term_years,
                                         future_value)

    @staticmethod
    def calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years, interest_type):
        monthly_interest_rate = annual_interest_rate / 12 / 100
        num_payments = loan_term_years * 12

        if interest_type == "simple":
            monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
        elif interest_type == "compound":
            monthly_payment = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / (
                        (1 + monthly_interest_rate) ** num_payments - 1)
        else:
            raise ValueError("Invalid interest type. Use 'simple' or 'compound'.")

        return monthly_payment

    @staticmethod
    def calculate_future_value(investment_amount, annual_return_rate, investment_term_years):
        future_value = investment_amount * (1 + annual_return_rate / 100) ** investment_term_years

        return future_value

    def save_investment_details(self, investment_type, amount, rate, term, result):
        self.master.geometry("400x400")
        with SessionLocal() as session:
            new_investment = Investment(
                account_number=self.user.account_number,
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                investment_type=investment_type,
                bond=amount if investment_type == "Bond/Home Loan" else 0,
                investment=amount if investment_type == "Investment" else 0,
                loan_amount=amount if investment_type == "Bond/Home Loan" else 0,
                annual_interest_rate=rate,
                loan_term_years=term,
                interest_type="simple",  # Change as needed
                monthly_payment=result if investment_type == "Bond/Home Loan" else 0
            )
            session.add(new_investment)
            session.commit()

    def view_statement(self):
        self.master.geometry("400x400")
        with SessionLocal() as session:
            transactions = session.query(Transaction).filter_by(account_number=self.user.account_number).all()

            if transactions:
                statement = "Transaction Statement:\n"
                for transaction in transactions:
                    statement += (f"{transaction.timestamp} - {transaction.deposits} Deposits, "
                                  f"{transaction.withdrawals} Withdrawals\n")

                messagebox.showinfo("Transaction Statement", statement)
            else:
                messagebox.showinfo("Transaction Statement", "No transactions found.")

    def view_balance(self):
        self.master.geometry("400x400")
        with SessionLocal() as session:
            transactions = session.query(Transaction).filter_by(account_number=self.user.account_number).all()
            current_balance = sum(transaction.deposits - transaction.withdrawals for transaction in transactions)

            messagebox.showinfo("Account Balance", f"Your Account Balance is: R{current_balance:.2f}")


if __name__ == "__main__":
    account_number = '123456'
    root = tk.Tk()
    app = BankingGUI(root, account_number)
    root.mainloop()
