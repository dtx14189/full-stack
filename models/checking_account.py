from decimal import Decimal
from .account import Account

class CheckingAccount(Account):
    """Represents a checking account in the bank. Checking accounts have a 0.08%
    interest rate, and can incur a $5.75 fee if balance is less than $100."""

    __mapper_args__ = {
        "polymorphic_identity": "Checking",
    }

    def __init__(self):
        super().__init__(Decimal('0.0008'))
    
    def _apply_fees(self):
        """If balance is less than $100, apply a fee of $5.75. Create a transaction
        with fee amount, and add it to list of transactions. The date for this transaction
        is the last day of the month that had the latest user-created transaction."""
        if(self.bal < Decimal('100')):
            self._add_transaction_end_of_month(Decimal('-5.75'))
    
    def __str__(self):
        return "Checking" + super().__str__()
        