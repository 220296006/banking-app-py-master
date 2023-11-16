# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/13
# @Time : 15:08


import hashlib
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

from models import User

Base = declarative_base()


def get_user_by_account_number(session: Session, account_number: int) -> User:
    return session.query(User).filter(User.account_number == account_number).first()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(Integer, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    password_confirmation = Column(String)

    transactions = relationship("Transaction", back_populates="user")
    investments = relationship("Investment", back_populates="user")
    forgot_passwords = relationship("ForgotPassword", back_populates="user")

    def verify_password(self, entered_password):
        hashed_entered_password = hashlib.sha256(entered_password.encode()).hexdigest()
        result = self.password == hashed_entered_password
        return result


# Transaction model
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(Integer, ForeignKey('users.id'))
    first_name = Column(String)
    last_name = Column(String)
    deposits = Column(Float)
    withdrawals = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")


# Investment model
class Investment(Base):
    __tablename__ = 'investments'

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(Integer, ForeignKey('users.id'))
    first_name = Column(String)
    last_name = Column(String)
    bond = Column(Float)
    investment = Column(Float)
    investment_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)  # Add this line
    loan_amount = Column(Float)
    annual_interest_rate = Column(Float)
    loan_term_years = Column(Integer)
    interest_type = Column(String)
    monthly_payment = Column(Float)

    user = relationship("User", back_populates="investments")


class ForgotPassword(Base):
    __tablename__ = 'forgot_passwords'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    email = Column(String, index=True)
    new_password = Column(String)

    # Relationship with the User model
    user = relationship("User", back_populates="forgot_passwords")


# SQLite database initialization
DATABASE_URL = "sqlite:///./BankData.db"
engine = create_engine(DATABASE_URL)

# In your code, before creating the engine and metadata, add the following line to drop the existing tables

# Drop existing tables (optional)

# Base.metadata.drop_all(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Session creation for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
