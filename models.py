# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/02
# @Time : 13:54

# User Class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


# Account Class
class Account:
    def __init__(self, user, account_number):
        self.user = user
        self.balance = 0
        self.account_number = account_number

    def view_balance(self):
        total_withdrawals = self.get_total_withdrawals()
        net_balance = self.balance - total_withdrawals
        return net_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    # Function to withdraw money from the account
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawal successful. New balance: {self.balance}")
            return True
        else:
            print(f"Invalid withdrawal amount or insufficient balance. Current balance: {self.balance}")
            return False

    def get_balance(self):
        return self.balance

    def get_total_withdrawals(self):
        with open("transaction_log.txt", "r") as log_file:
            lines = log_file.readlines()
            total_withdrawals = 0

            in_user_transactions = False
            for line in lines:
                if in_user_transactions:
                    if line.startswith("Username:"):
                        # Reached the end of user transactions
                        break
                    elif line.startswith("## Withdrawals ##"):
                        # Start of a withdrawal block
                        continue
                    elif line.startswith("Amount: $"):
                        amount = float(line.split("$")[1].strip())
                        total_withdrawals += amount
                if f"Account Number: {self.account_number}" in line:
                    in_user_transactions = True

        return total_withdrawals


# Invest Class
class Invest:
    def __init__(self, account, amount, invest_type, start_date):
        self.account = account
        self.amount = amount
        self.invest_type = invest_type
        self.start_date = start_date
