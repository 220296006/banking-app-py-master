# @Author : Thabiso Matsaba
# @Project : banking-app-py-master
# @Date:  2023/11/13
# @Time : 15:08
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


# User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    gender = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    passwordConfirmation = Column(String)

    transactions = relationship("Transaction", back_populates="user")
    investments = relationship("Investment", back_populates="user")


# Transaction model
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    accountNumber = Column(Integer, ForeignKey('users.id'))
    firstName = Column(String)
    lastName = Column(String)
    deposits = Column(Float)
    withdrawals = Column(Float)

    user = relationship("User", back_populates="transactions")


# Investment model
class Investment(Base):
    __tablename__ = 'investments'

    id = Column(Integer, primary_key=True, index=True)
    accountNumber = Column(Integer, ForeignKey('users.id'))
    bond = Column(Float)
    investment = Column(Float)

    user = relationship("User", back_populates="investments")


# SQLite database initialization
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Session creation for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
