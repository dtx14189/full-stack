from decimal import Decimal, ROUND_HALF_UP

class Transaction:
    """Represent a transaction, which is either a deposit, withdrawal, interest, or a few.
    A transaction has an amount, a date, and boolean indicating whether it is an interest/fee."""
    def __init__(self, amount, date, is_interest_fee):
        self._amount = amount
        self._date = date
        self._is_interest_fee = is_interest_fee
    
    def is_exempt(self):
        """Check if the transaction is exempt from account limits"""
        return self._is_interest_fee
    
    def date_matches(self, other_date):
        """Determine if this transaction has the same date as another date. 
        This transaction must also not be an interest or fee."""
        return (self._date == other_date)
    
    def month_matches(self, other_date):
        """Determine if this transaction has the same month as another date. 
        This transaction must also not be an interest or fee."""
        return (self._date.month == other_date.month) and (self._date.year == other_date.year)
    
    def __lt__(self, other):
        return self._date < other._date

    def __str__(self):
        rounded_amt = self._amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"{self._date}, ${rounded_amt:,.2f}"
    