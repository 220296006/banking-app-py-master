# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/14
# @Time : 10:10

import tkinter as tk
from tkinter import messagebox, simpledialog, font, ttk

from database import SessionLocal, Transaction, get_user_by_account_number, Investment


class BankingGUI:
    def __init__(self, master, account_number):
        self.user = None
        self.current_balance = None
        self.master = master
        self.master.title("Banking App")
        self.load_user_data(account_number)
        self.master.geometry("600x600")
        self.master.configure(bg='gray')

        button_height = 2
        button_width = 20

        # Use Ubuntu font
        ubuntu_font = font.Font(family="Ubuntu", size=16)

        button_style = ttk.Style()
        button_style.configure("TButton", padding=(10, 5), font=('Ubuntu', 12), background='blue', foreground='black')

        # Welcome message
        if self.user:
            self.label_welcome = tk.Label(master, text=f"Welcome {self.user.first_name} {self.user.last_name}!")
            self.label_welcome.pack(pady=20)

            # Account balance
            self.label_balance = tk.Label(master, text=f"Your Account Balance is: R{self.current_balance:.2f}")
            self.label_balance.pack(pady=20)

            # Transaction button
            self.btn_transaction = tk.Button(master, text="Transaction", command=self.show_transaction_options,
                                             width=button_width, height=button_height)
            self.btn_transaction.pack(pady=20, padx=10)

            # Investment button
            self.btn_investment = tk.Button(master, text="Investment", command=self.show_investment_options,
                                            width=button_width, height=button_height)
            self.btn_investment.pack(pady=20, padx=10)

            # Statement button
            self.btn_statement = tk.Button(master, text="Statement", command=self.view_statement,
                                           width=button_width, height=button_height)
            self.btn_statement.pack(pady=20, padx=10)

            # View Balance button
            self.btn_view_balance = tk.Button(master, text="View Balance", command=self.view_balance,
                                              width=button_width, height=button_height)
            self.btn_view_balance.pack(pady=20, padx=10)

            # Exit button
            self.btn_exit = tk.Button(master, text="Exit", command=self.exit_system,
                                      width=button_width, height=button_height)
            self.btn_exit.pack(pady=20, padx=10)

            self.btn_view_balance = tk.Button(master, text="View Balance", command=self.view_balance, width=20,
                                              height=2)
            self.btn_view_balance.pack(pady=20)

            self.btn_exit = tk.Button(master, text="Exit", command=self.exit_system, width=20, height=2)
            self.btn_exit.pack(pady=20)

        else:
            messagebox.showerror("Error", "User not found. Unable to load data.")

    def exit_system(self):
        self.master.destroy()

    def load_user_data(self, account_number):
        with SessionLocal() as session:
            self.user = get_user_by_account_number(session, account_number)

            if self.user:
                transactions = session.query(Transaction).filter_by(account_number=account_number).all()
                self.current_balance = sum(
                    transaction.deposits - transaction.withdrawals for transaction in transactions)

    def show_transaction_options(self):
        options = "Choose an option:\n1. Deposit\n2. Withdrawal"
        custom_dialog = tk.Toplevel(self.master)
        custom_dialog.title("Transaction Options")
        custom_dialog.geometry("400x300")
        custom_dialog.configure(bg='gray')

        label = tk.Label(custom_dialog, text=options, font=("Ubuntu", 12))
        label.pack(pady=10)

        entry_var = tk.StringVar()
        entry = tk.Entry(custom_dialog, textvariable=entry_var, font=("Ubuntu", 12), width=30)
        entry.pack(pady=10)

        confirm_button = tk.Button(custom_dialog, text="Confirm",
                                   command=lambda: self.handle_transaction_choice(entry_var.get(), custom_dialog),
                                   font=("Ubuntu", 12))
        confirm_button.pack(pady=10)

    def handle_transaction_choice(self, choice, dialog):
        try:
            choice = int(choice)
        except ValueError:
            messagebox.showerror("Error", "Invalid choice. Please enter a number.")
            return

        if choice == 1:
            self.perform_deposit()
        elif choice == 2:
            self.perform_withdrawal()

        dialog.destroy()
        self.master.geometry("400x400")
        self.master.update()
        self.master.configure(bg='gray')

    def perform_deposit(self):
        try:
            deposit_amount = simpledialog.askfloat("Deposit", "Enter deposit amount:")
            if deposit_amount is None:
                messagebox.showinfo("Info", "Deposit canceled.")
                return  # User canceled the input dialog
        except ValueError:
            messagebox.showerror("Error", "Invalid deposit amount. Please enter a valid number.")
            return

        if deposit_amount <= 0:
            messagebox.showerror("Error", "Invalid deposit amount. Please enter a positive amount.")
            return

        custom_dialog = tk.Toplevel(self.master)
        custom_dialog.title("Deposit Confirmation")
        custom_dialog.geometry("400x300")
        custom_dialog.configure(bg='gray')

        label_text = f"Confirm deposit of R{deposit_amount:.2f}?"
        label = tk.Label(custom_dialog, text=label_text, font=("Ubuntu", 12))
        label.pack(pady=10)

        entry_var = tk.StringVar()
        entry = tk.Entry(custom_dialog, textvariable=entry_var, font=("Ubuntu", 12), width=30)
        entry.pack(pady=10)

        confirm_button = tk.Button(custom_dialog, text="Confirm",
                                   command=lambda: self.handle_deposit_confirmation(deposit_amount, entry_var.get(),
                                                                                    custom_dialog), font=("Ubuntu", 12))
        confirm_button.pack(pady=10)

    def handle_deposit_confirmation(self, deposit_amount, choice, dialog):
        if choice.lower() == 'yes':
            self.update_transaction_log(deposit_amount, 0)
        dialog.destroy()
        self.master.geometry("400x400")
        self.master.update()
        self.master.configure(bg='gray')

    def perform_withdrawal(self):
        try:
            withdrawal_amount = simpledialog.askfloat("Withdrawal", "Enter withdrawal amount:")
            if withdrawal_amount is None:
                messagebox.showinfo("Info", "Withdrawal canceled.")
                return  # User canceled the input dialog
        except ValueError:
            messagebox.showerror("Error", "Invalid withdrawal amount. Please enter a valid number.")
            return

        if withdrawal_amount <= 0:
            messagebox.showerror("Error", "Invalid withdrawal amount. Please enter a positive amount.")
            return

        custom_dialog = tk.Toplevel(self.master)
        custom_dialog.title("Withdrawal Confirmation")
        custom_dialog.geometry("400x400")
        custom_dialog.configure(bg='gray')

        label_text = f"Confirm withdrawal of R{withdrawal_amount:.2f}?"
        label = tk.Label(custom_dialog, text=label_text, font=("Ubuntu", 12))
        label.pack(pady=10)

        entry_var = tk.StringVar()
        entry = tk.Entry(custom_dialog, textvariable=entry_var, font=("Ubuntu", 12), width=30)
        entry.pack(pady=10)
        confirm_button = tk.Button(custom_dialog, text="Confirm",
                                   command=lambda: self.handle_withdrawal_confirmation(withdrawal_amount,
                                                                                       entry_var.get(), custom_dialog),
                                   font=("Ubuntu", 12))
        confirm_button.pack(pady=10)

    def handle_withdrawal_confirmation(self, withdrawal_amount, choice, dialog):
        if choice.lower() == 'yes':
            self.update_transaction_log(0, withdrawal_amount)
        dialog.destroy()
        self.master.geometry("400x400")
        self.master.update()
        self.master.configure(bg='gray')

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
            self.master.geometry("600x600")
            self.master.update()

    def show_investment_options(self):
        options = "Choose an option:\n1. Bond/Home Loan\n2. Invest Calculators"
        custom_dialog = tk.Toplevel(self.master)
        custom_dialog.title("Investment Options")
        custom_dialog.geometry("400x300")
        custom_dialog.configure(bg='gray')

        label = tk.Label(custom_dialog, text=options, font=("Ubuntu", 12))
        label.pack(pady=10)

        entry_var = tk.StringVar()
        entry = tk.Entry(custom_dialog, textvariable=entry_var, font=("Ubuntu", 12), width=30)
        entry.pack(pady=10)

        confirm_button = tk.Button(custom_dialog, text="Confirm",
                                   command=lambda: self.handle_investment_confirmation(entry_var.get(), custom_dialog),
                                   font=("Ubuntu", 12))
        confirm_button.pack(pady=10)

    def handle_investment_confirmation(self, choice, dialog):
        try:
            choice = int(choice)
        except ValueError:
            messagebox.showerror("Error", "Invalid choice. Please enter a number.")
            return

        if choice == 1:
            self.perform_bond_loan_calculation()
        elif choice == 2:
            self.perform_investment_calculation()

        dialog.destroy()
        self.master.geometry("400x400")
        self.master.update()
        self.master.configure(bg='gray')

    def perform_bond_loan_calculation(self):
        try:
            loan_amount = simpledialog.askfloat("Bond/Home Loan", "Enter loan amount:")
            interest_rate = simpledialog.askfloat("Bond/Home Loan", "Enter annual interest rate:")
            loan_term_years = simpledialog.askinteger("Bond/Home Loan", "Enter loan term (in years):")
            if any(arg is None for arg in (loan_amount, interest_rate, loan_term_years)):
                messagebox.showinfo("Info", "Loan calculation canceled.")
                return  # User canceled the input dialog
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
            return

        if loan_amount <= 0 or interest_rate <= 0 or loan_term_years <= 0:
            messagebox.showerror("Error", "Invalid input. Please enter positive values.")
            return

        custom_dialog = tk.Toplevel(self.master)
        custom_dialog.title("Loan Calculation Confirmation")
        custom_dialog.geometry("400x400")

        label_text = "Confirm your loan details?"
        label = tk.Label(custom_dialog, text=label_text, font=("Ubuntu", 12))
        label.pack(pady=10)

        entry_var = tk.StringVar()
        entry = tk.Entry(custom_dialog, textvariable=entry_var, font=("Ubuntu", 12), width=30)
        entry.pack(pady=10)

        confirm_button = tk.Button(custom_dialog, text="Confirm",
                                   command=lambda: self.handle_loan_details_confirmation(loan_amount, interest_rate,
                                                                                         loan_term_years,
                                                                                         entry_var.get(),
                                                                                         custom_dialog),
                                   font=("Ubuntu", 12))
        confirm_button.pack(pady=10)

    def handle_loan_details_confirmation(self, loan_amount, interest_rate, loan_term_years, user_input, dialog):
        try:
            user_input = user_input.strip().lower()
            if user_input != 'yes':
                messagebox.showinfo("Info", "Loan details confirmation canceled.")
                return  # Confirmation canceled by the user
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter 'yes' to confirm or leave it blank to cancel.")
            return

        interest_type = simpledialog.askstring("Interest Type", "Enter interest type (simple/compound):")
        if not interest_type or interest_type.lower() not in ["simple", "compound"]:
            messagebox.showerror("Error", "Invalid interest type. Please enter 'simple' or 'compound'.")
            dialog.destroy()
            self.master.geometry("600x600")
            self.master.update()
            return

        monthly_payment = self.calculate_monthly_payment(loan_amount, interest_rate, loan_term_years, interest_type)
        self.save_investment_details("Bond/Home Loan", loan_amount, interest_rate, loan_term_years, monthly_payment)

        dialog.destroy()
        self.master.geometry("600x600")
        self.master.update()

    def perform_investment_calculation(self):
        try:
            investment_amount = simpledialog.askfloat("Investment", "Enter investment amount:")
            annual_return_rate = simpledialog.askfloat("Investment", "Enter annual return rate:")
            investment_term_years = simpledialog.askinteger("Investment", "Enter investment term (in years):")
            if any(arg is None for arg in (investment_amount, annual_return_rate, investment_term_years)):
                messagebox.showinfo("Info", "Investment calculation canceled.")
                return  # User canceled the input dialog
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
            return

        if investment_amount <= 0 or annual_return_rate <= 0 or investment_term_years <= 0:
            messagebox.showerror("Error", "Invalid input. Please enter positive values.")
            return

        custom_dialog = tk.Toplevel(self.master)
        custom_dialog.title("Investment Calculation Confirmation")
        custom_dialog.geometry("400x300")

        label_text = "Confirm your investment details?"
        label = tk.Label(custom_dialog, text=label_text, font=("Ubuntu", 12))
        label.pack(pady=10)

        entry_var = tk.StringVar()
        entry = tk.Entry(custom_dialog, textvariable=entry_var, font=("Ubuntu", 12), width=30)
        entry.pack(pady=10)

        confirm_button = tk.Button(custom_dialog, text="Confirm",
                                   command=lambda: self.handle_investment_details_confirmation(investment_amount,
                                                                                               annual_return_rate,
                                                                                               investment_term_years,
                                                                                               entry_var.get(),
                                                                                               custom_dialog),
                                   font=("Ubuntu", 12))
        confirm_button.pack(pady=10)

    def handle_investment_details_confirmation(self, investment_amount, annual_return_rate, investment_term_years,
                                               user_input, dialog):
        try:
            user_input = user_input.strip().lower()
            if user_input != 'yes':
                messagebox.showinfo("Info", "Investment details confirmation canceled.")
                return  # Confirmation canceled by the user
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter 'yes' to confirm or leave it blank to cancel.")
            return

        future_value = self.calculate_future_value(investment_amount, annual_return_rate, investment_term_years)
        self.save_investment_details("Investment", investment_amount, annual_return_rate, investment_term_years,
                                     future_value)

        dialog.destroy()
        self.master.geometry("600x600")
        self.master.update()

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
        with SessionLocal() as session:
            transactions = session.query(Transaction).filter_by(account_number=self.user.account_number).all()
            custom_dialog = tk.Toplevel(self.master)
            custom_dialog.title("Transaction Statement")
            custom_dialog.geometry("600x400")

            text_widget = tk.Text(custom_dialog, wrap="word", font=("Helvetica", 12))
            text_widget.pack(expand=True, fill="both", padx=10, pady=10)

            if transactions:
                user_info = (f"{self.user.first_name} {self.user.last_name} - Account Number: "
                             f"{self.user.account_number}\n")
                statement = "Transaction Statement:\n\n" + user_info

                for transaction in transactions:
                    # Format date and time with hours and minutes only
                    formatted_timestamp = transaction.timestamp.strftime("%Y-%m-%d %H:%M")

                    transaction_str = f"{formatted_timestamp} -"
                    if transaction.deposits > 0:
                        transaction_str += f" {transaction.deposits} Deposit,"
                    if transaction.withdrawals > 0:
                        transaction_str += f" {transaction.withdrawals} Withdrawal,"

                    # Remove trailing comma and add a line break
                    transaction_str = transaction_str.rstrip(",") + "\n\n"

                    statement += transaction_str

                text_widget.insert("1.0", statement)
            else:
                text_widget.insert("1.0", "No transactions found.")

            close_button = tk.Button(custom_dialog, text="Close", command=custom_dialog.destroy, font=("Ubuntu", 12))
            close_button.pack(pady=10)

        self.master.geometry("600x600")
        self.master.update()

    def view_balance(self):
        with SessionLocal() as session:
            transactions = session.query(Transaction).filter_by(account_number=self.user.account_number).all()
            current_balance = sum(transaction.deposits - transaction.withdrawals for transaction in transactions)

            messagebox.showinfo("Account Balance", f"Your Account Balance is: R{current_balance:.2f}")

        self.master.geometry("400x400")
        self.master.update()


if __name__ == "__main__":
    account_number = '123456'
    root = tk.Tk()
    app = BankingGUI(root, account_number)
    root.mainloop()
