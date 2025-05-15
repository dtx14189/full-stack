from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .account import Account
from .checking_account import CheckingAccount
from .savings_account import SavingsAccount
from .transaction import Transaction
