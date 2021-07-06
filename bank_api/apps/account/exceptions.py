class TransferValidationError(Exception):
	'''Raised when account_from and account_to are equal'''
	pass


class BalanceValidationError(Exception):
	'''Raised when account_from < amount'''
	pass