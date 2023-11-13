# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/13
# @Time : 15:08
import hashlib
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


# User model
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

    def verify_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return self.password == hashed_password


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


# SQLite database initialization
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

# In your code, before creating the engine and metadata, add the following line to drop the existing tables

# Drop existing tables (optional)

#Base.metadata.drop_all(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Session creation for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
