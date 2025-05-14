from decimal import Decimal, ROUND_HALF_UP
from . import db

class Transaction(db.Model):
    """Represent a transaction, which is either a deposit, withdrawal, interest, or a few.
    A transaction has an amount, a date, and boolean indicating whether it is an interest/fee."""

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts._id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    is_interest_fee = db.Column(db.Integer, nullable=False)

    def __init__(self, amount, date, is_interest_fee, account):
        self.amount = amount
        self.date = date
        self.is_interest_fee = is_interest_fee
        self.account = account
    
    def is_exempt(self):
        """Check if the transaction is exempt from account limits"""
        return self.is_interest_fee
    
    def date_matches(self, other_date):
        """Determine if this transaction has the same date as another date. 
        This transaction must also not be an interest or fee."""
        return (self.date == other_date)
    
    def month_matches(self, other_date):
        """Determine if this transaction has the same month as another date. 
        This transaction must also not be an interest or fee."""
        return (self.date.month == other_date.month) and (self.date.year == other_date.year)
    
    def describe(self):
        """Describe a single transaction with its date and amount."""
        rounded_amt = self.amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return {
            "amount": str(rounded_amt),
            "date": str(self.date)
        }
    
    def get_date(self):
        return self.date
    
    def __lt__(self, other):
        return self.date < other._date

    def __str__(self):
        rounded_amt = self.amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"{self.date}, ${rounded_amt:,.2f}"
    