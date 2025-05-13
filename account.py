import calendar
import logging
import exceptions
from decimal import Decimal, ROUND_HALF_UP
from transaction import Transaction
from datetime import datetime

    
class Account:
    """Represent an account in the bank. An account has an id, a balance, 
    and a list of transactions."""

    def __init__(self, type: str, acct_id, interest_rate):
        self._type = type
        self._id = acct_id
        self._interest_rate = interest_rate
        self._bal = Decimal('0')
        self._transactions = []
        self._latest_date = None
    
    def deposit_withdraw(self, amount, date):
        """Deposit/Withdraw from this account. A positive amount is a deposit, 
        and a negative amount is a withdraw. Create a transaction with the amount 
        and date, and add it to list of transactions.
        
        Only performs withdrawal if resulting balance is non-negative."""
        if(self._bal + amount < Decimal('0')):
            raise exceptions.OverdrawError()
        else:
            if self._transactions:
                if date < self._latest_date:
                    raise exceptions.TransactionSequenceError(self._latest_date)    
            self._add_transaction(amount, date, False)
        
    def apply_interest_fees(self):
        """(1) Apply interest to balance at a this account's rate. Create a transaction with 
        interest amount, and add it to list of transactions. The date for this transaction 
        is the last day of the month that had the latest user-created transaction.
        
        (2) If applicable, apply fees to balance. If fees are applied, create a transaction
        with fee amount, and add it to list of transactions. The date for this transaction
        is the last day of the month that had the latest user-created transaction."""
        last_day_of_latest_month = self._find_last_day_of_month()
        for transaction in self._transactions:
            if transaction.date_matches(last_day_of_latest_month) and transaction.is_exempt():
                raise exceptions.TransactionSequenceError(last_day_of_latest_month)

        self._apply_interest()
        self._apply_fees()
        logging.debug("Triggered interest and fees")

    def _apply_interest(self):
        
        interest = self._bal * self._interest_rate
        self._add_transaction_end_of_month(interest)
        
    def _apply_fees(self):
        pass

    def list_transactions(self):
        """Print all transactions (date and amount) in this account."""
        for transaction in self._transactions:
            print(transaction)

    def describe_transactions(self):
        """Describe all transactions with date and amount."""
        return [transaction.describe() for transaction in self._transactions]

    def id_matches(self, id):
        """Determine if this account has the given id"""
        return self._id == int(id)
    
    def _add_transaction(self, amount, date, is_interest_fee):
        transaction = Transaction(amount, date, is_interest_fee)
        self._transactions.append(transaction)
        self._transactions.sort()
        if self._latest_date is None:
            self._latest_date = date
        elif date > self._latest_date:
            self._latest_date = date
        self._set_bal(self._bal + amount)
        logging.debug(f"Created transaction: {self._id}, {amount}")

    def _add_transaction_end_of_month(self, amount):
        last_day_of_latest_month = self._find_last_day_of_month()
        self._add_transaction(amount, last_day_of_latest_month, True)
    
    def _find_last_day_of_month(self):
        days_in_latest_month = calendar.monthrange(self._latest_date.year, self._latest_date.month)[1] 
        return datetime(self._latest_date.year, self._latest_date.month, days_in_latest_month).date()
    
    def _set_bal(self, new_bal):
        self._bal = new_bal
    
    def get_bal(self):
        return self._bal
    
    def describe(self):
        """Describe a single account with its type, id, and balance."""
        rounded_bal = self._bal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return {
            "type": self._type,
            "id": self._id,
            "balance": str(rounded_bal)
        }

    def __str__(self):
        rounded_bal = self._bal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"#{self._id:09d},\tbalance: ${rounded_bal:,.2f}"