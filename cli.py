import os
import sys
import pickle
import logging
import exceptions
from bank import Bank
from datetime import datetime 
from decimal import Decimal, InvalidOperation

class CLI:
    """Represent the bank command line interface, which responds to choices when run."""

    def __init__(self):
        self._load()

    def _load(self):
        if os.path.exists("bank.pickle"):
            with open("bank.pickle", "rb") as file:
                self._bank = pickle.load(file)
                logging.debug("Loaded from bank.pickle")
        else:
            self._bank = Bank()
        self._selected_acct = None

    def _display_menu(self):
        print(
            f"""--------------------------------
Currently selected account: {self._selected_acct}
Enter command
1: open account
2: summary
3: select account
4: add transaction
5: list transactions
6: interest and fees
7: quit"""
        )

    def run(self):
        """Display the bank commnad line interface and respond to choices until the user quits."""
        while True:
            self._display_menu()
            choice = input(">")
            if choice == "1":
                self._open_account()
            elif choice == "2":
                self._summarize()
            elif choice == "3":
                self._select_account()
            elif choice == "4":
                if self._selected_acct: 
                    self._add_transaction()
                else: 
                    print("This command requires that you first select an account.")
            elif choice == "5":
                self._list_transactions()
            elif choice == "6":
                self._apply_interest_fees()
            elif choice == "7":
                self._quit()
    
    def _open_account(self):
        print("Type of account? (checking/savings)")
        account_type = input(">")
        self._bank.add_account(account_type)
    
    def _summarize(self):
        self._bank.list_accounts()

    def _select_account(self):
        print("Enter account number")
        account_id = input(">")
        self._selected_acct = self._bank.find_account(account_id)

    def _add_transaction(self):
        while True:
            print("Amount?")
            amount_str = input(">")
            try:
                amount = Decimal(amount_str)
                break
            except InvalidOperation:
                print("Please try again with a valid dollar amount.")
        
        while True:
            print("Date? (YYYY-MM-DD)")
            date_str = input(">")
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date() 
                break
            except ValueError:
                print("Please try again with a valid date in the format YYYY-MM-DD.")

        try:
            self._selected_acct.deposit_withdraw(amount, date) 
        except exceptions.OverdrawError:
            print("This transaction could not be completed due to an insufficient account balance.")
        except exceptions.TransactionLimitError as limit_error:
            if limit_error.hit_daily_limit:
                print("This transaction could not be completed because this account already has 2 transactions in this day.")
            else:
                print("This transaction could not be completed because this account already has 5 transactions in this month.")
        except exceptions.TransactionSequenceError as sequence_error:
            print(f"New transactions must be from {(sequence_error.latest_date).strftime('%Y-%m-%d')} onward.")

    def _list_transactions(self):
        try: 
            self._selected_acct.list_transactions()
        except AttributeError:
            print("This command requires that you first select an account.")
    
    def _apply_interest_fees(self):
        try:
            self._selected_acct.apply_interest_fees()
        except AttributeError:
            print("This command requires that you first select an account.")
        except exceptions.TransactionSequenceError as sequence_error:
            print(f"Cannot apply interest and fees again in the month of {(sequence_error.latest_date).strftime('%B')}.")
    
    def _quit(self):
        self._save()
        logging.debug("Saved to bank.pickle")
        sys.exit(0)

    def _save(self):
        with open("bank.pickle", "wb") as file:
            pickle.dump(self._bank, file)

if __name__ == "__main__":
    logging.basicConfig(filename='bank.log',
                        level=logging.DEBUG, 
                        format='%(asctime)s|%(levelname)s|%(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S")
    try:
        CLI().run()
    except Exception as e:
        print("Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
        logging.error(f"{type(e).__name__}: {repr(str(e))}")


