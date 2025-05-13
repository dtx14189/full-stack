import logging
from checking_account import CheckingAccount
from savings_account import SavingsAccount
from account import Account

class Bank:
    """Represent a collection of accounts."""

    def __init__(self):
        self._accounts = []
        self._num_accts = 0
    
    def add_account(self, type):
        """Create a new account (checking or savings) and add it to the list"""
        self._num_accts += 1
        if type == "checking":
            new_account = CheckingAccount(self._num_accts)
        elif type == "savings":
            new_account = SavingsAccount(self._num_accts)
        self._accounts.append(new_account)
        logging.debug(f"Created account: {self._num_accts}")
    
    def list_accounts(self):
        """Print all accounts in the bank."""
        for account in self._accounts:
            print(account)
    
    def find_account(self, account_id) -> Account:
        """Locate the account with the given id.
        Returns None if no matching account is found."""
        for account in self._accounts:
            if account.id_matches(account_id):
                return account
        return None

    def describe_accounts(self) -> list[dict]:
        """Describe all accounts with type, id, and balance"""
        return [account.describe() for account in self._accounts]