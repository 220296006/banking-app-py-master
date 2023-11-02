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
    def __init__(self, user, balance=0.0):
        self.user = user
        self.balance = balance

    def view_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

# Invest Class
class Invest:
    def __init__(self, account, amount, invest_type, start_date):
        self.account = account
        self.amount = amount
        self.invest_type = invest_type
        self.start_date = start_date
