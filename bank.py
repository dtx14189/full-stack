import logging
from uuid import uuid4

from models import db, Account, CheckingAccount, SavingsAccount

class Bank:
    """Interface to interact with a persistent collection of accounts."""

    def __init__(self):
        self._accounts = []
    
    def add_account(self, type: str) -> Account:
        """Create a new account (checking or savings) and save it to the database"""

        account_id = str(uuid4())
        if type == "checking":
            new_account = CheckingAccount(account_id)
        elif type == "savings":
            new_account = SavingsAccount(account_id)
        
        db.session.add(new_account)
        db.session.commit()

        logging.debug(f"Created account: {account_id}")
    
    def find_account(self, account_id) -> Account:
        """Locate the account with the given id.
        Returns None if no matching account is found."""
        return Account.query.get(account_id)

    def describe_accounts(self) -> list[dict]:
        """Describe all accounts with type, id, and balance"""
        accounts: list[Account] = Account.query.all()
        return [account.describe() for account in accounts]
    
    def list_accounts(self):
        """Print all accounts in the bank."""
        accounts: list[Account] = Account.query.all()
        for account in accounts:
            print(account)
    