import calendar
import logging
import exceptions
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from .transaction import Transaction
from . import db
from sqlalchemy.orm import relationship

class Account(db.Model):
    """Represent an account in the bank. An account has an id, a balance, 
    and a list of transactions."""

    __tablename__ = "accounts"
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    interest_rate = db.Column(db.Numeric(5, 4), nullable=False)
    bal = db.Column(db.Numeric(10, 2), nullable=False)
    transactions = relationship(
        "Transaction", 
        backref="account", 
        lazy=True, 
        cascade="all, delete-orphan",
        order_by=Transaction.date.desc()
    )

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "account",
    }

    def __init__(self, interest_rate):
        self.interest_rate = interest_rate
        self.bal = Decimal('0')
    
    def deposit_withdraw(self, amount, date):
        """Deposit/Withdraw from this account. A positive amount is a deposit, 
        and a negative amount is a withdraw. Create a transaction with the amount 
        and date, and add it to list of transactions.
        
        Only performs withdrawal if resulting balance is non-negative."""
        if(self.bal + amount < Decimal('0')):
            raise exceptions.OverdrawError()
        else:
            if self.transactions:
                latest_date = self._get_latest_date()
                if latest_date is not None and date < self._get_latest_date():
                    raise exceptions.TransactionSequenceError(self._get_latest_date())    
            self._add_transaction(amount, date, False)
        
    def apply_interest_fees(self):
        """(1) Apply interest to balance at a this account's rate. Create a transaction with 
        interest amount, and add it to list of transactions. The date for this transaction 
        is the last day of the month that had the latest user-created transaction.
        
        (2) If applicable, apply fees to balance. If fees are applied, create a transaction
        with fee amount, and add it to list of transactions. The date for this transaction
        is the last day of the month that had the latest user-created transaction."""
        if not self.transactions:
            return 
        
        last_day_of_latest_month = self._find_last_day_of_month()
        for transaction in self.transactions:
            if transaction.date_matches(last_day_of_latest_month) and transaction.is_exempt():
                raise exceptions.TransactionSequenceError(last_day_of_latest_month)

        self._apply_interest()
        self._apply_fees()
        logging.debug("Triggered interest and fees")

    def _apply_interest(self):
        interest = self.bal * self.interest_rate
        self._add_transaction_end_of_month(interest)
        
    def _apply_fees(self):
        pass

    def list_transactions(self):
        """Print all transactions (date and amount) in this account."""
        for transaction in self.transactions:
            print(transaction)

    def describe_transactions(self):
        """Describe all transactions with date and amount."""
        return [transaction.describe() for transaction in self.transactions]

    def id_matches(self, id):
        """Determine if this account has the given id"""
        return self.id == int(id)
    
    def get_id(self):
        return self.id
    
    def _add_transaction(self, amount, date, is_interest_fee):
        transaction = Transaction(amount, date, is_interest_fee, account=self)
        self.bal += amount
        db.session.add(self)
        db.session.add(transaction)
        db.session.commit()
        logging.debug(f"Created transaction: {self.id}, {amount}")

    def _add_transaction_end_of_month(self, amount):
        last_day_of_latest_month = self._find_last_day_of_month()
        self._add_transaction(amount, last_day_of_latest_month, True)
    
    def _find_last_day_of_month(self):
        latest_date = self._get_latest_date()
        days_in_latest_month = calendar.monthrange(latest_date.year, latest_date.month)[1] 
        return datetime(latest_date.year, latest_date.month, days_in_latest_month).date()
    
    def _get_latest_date(self):
        return self.transactions[0].get_date() if self.transactions else None
    
    def get_bal(self):
        return self.bal
    
    def describe(self):
        """Describe a single account with its type, id, and balance."""
        rounded_bal = self.bal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return {
            "type": self.type,
            "id": self.id,
            "balance": str(rounded_bal)
        }

    def __str__(self):
        rounded_bal = self.bal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"#{self.id:09d},\tbalance: ${rounded_bal:,.2f}"
