class TransferValidationError(Exception):
    '''Raised when account_from and account_to are equal'''
    
    def __init__(self, account_from, account_to):   
        self.account_from = account_from
        self.account_to = account_to
    
    def __str__(self):
        return ('ensure {} is not equal to {}').format(
            self.account_from, self.account_to
        )
    


class BalanceValidationError(Exception):
    '''Raised when balance < amount'''
    
    def __init__(self, balance, amount):   
        self.balance = balance
        self.amount = amount
    
    def __str__(self):
        return ('ensure, that your balance = {} '
            'is not less than transfer amount = {}').format(
            self.balance, self.amount
        )