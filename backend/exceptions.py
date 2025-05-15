class OverdrawError(Exception):
    """Represents the exception from overdrawing the account (i.e. making the balance negative)"""
    pass

class TransactionSequenceError(Exception):
    """Represents the exception from adding transactions out of order, 
    or applying interest/fees more than once in a month."""
    def __init__(self, latest_date):
        self.latest_date = latest_date

class TransactionLimitError(Exception):
    """Represents the exception from exceeding transaction limits (daily/monthly)"""
    def __init__(self, hit_daily_limit):
        self.hit_daily_limit = hit_daily_limit

