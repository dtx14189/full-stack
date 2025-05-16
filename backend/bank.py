import logging
from models import db, Account, CheckingAccount, SavingsAccount

class Bank:
    """Interface to interact with a persistent collection of accounts."""

    def add_account(self, type: str) -> Account:
        """Create a new account (checking or savings) and save it to the database"""

        if type == "checking":
            new_account = CheckingAccount()
        elif type == "savings":
            new_account = SavingsAccount()
        
        db.session.add(new_account)
        db.session.commit()

        logging.debug(f"Created account with {new_account.get_id()}")
    
    def find_account(self, account_id) -> Account:
        """Locate the account with the given id.
        Returns None if no matching account is found."""
        return Account.query.get(account_id)

    def describe_accounts(self) -> list[dict]:
        """Describe all accounts with type, id, and balance"""
        accounts: list[Account] = Account.query.order_by(Account.id).all()
        return [account.describe() for account in accounts]
    
    def list_accounts(self):
        """Print all accounts in the bank."""
        accounts: list[Account] = Account.query.all()
        for account in accounts:
            print(account)
    