import exceptions
from decimal import Decimal
from account import Account

class SavingsAccount(Account):
    """Represent a savings account in the bank. Savings accounts have a 0.33%
    interest rate. 
    
    Additionally, savings accounts have a transaction limit of 2 transactions per day
    and 5 transactions per month. That is, if adding a transaction exceeds one of these 
    limits, the transaction is void. Interest does not count towards this limit, and 
    bypasses this limit."""

    def __init__(self, acct_id):
        super().__init__(acct_id, Decimal("0.0033"))

    def deposit_withdraw(self, amount, date):
        """Check if an additional transaction on given date exceeds transaction limits. If not,
        deposit/withdraw from this account. A positive amount is a deposit, 
        and a negative amount is a withdraw. Create a transaction with the amount 
        and date, and add it to list of transactions. 

        Only performs withdrawal if resulting balance is non-negative."""
        if(self._check_transaction_limit(date)):
            super().deposit_withdraw(amount, date)
    
    def _check_transaction_limit(self, date_to_add):
        same_date = 2 # limit on # of transactions with same date
        same_month = 5 # limit on # of transactions with same month

        for transaction in self._transactions:
            if transaction.date_matches(date_to_add) and (not transaction.is_exempt()): # same date
                same_date -= 1
            if transaction.month_matches(date_to_add) and (not transaction.is_exempt()): # same month
                same_month -= 1
        
        if same_date == 0:
            raise exceptions.TransactionLimitError(True)
        if same_month == 0:
            raise exceptions.TransactionLimitError(False)

        return ((same_month > 0) and (same_date > 0))
            

    def __str__(self):
        return "Savings" + super().__str__()
