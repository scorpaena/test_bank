Abstract
--------
This is a simple training bank application.
It is made using Django/DRF framework and represents simple application, where the employees can register customer and create bank account with initial deposit. Employees can transfer money between different accounts.
For data storage the Python standard SQLite database is used (to make it simpler to run during the check).

Requirements
------------
1. Install all the required modules:
  `pip install -r requirements`
2. Run the migration:
  `python manage.py migrate`
3. The project uses default insecure SECRET_KEY. To make it secure, create `.env` file according to the `.env.example`. Also refer to [this link](https://www.youtube.com/watch?v=5iWhQWVXosU&t=0s) for detailed information (note: for Ubuntu use `.bashrc` instead of `.bash_profile`).

Instructions
------------
1. Create an employee:
  `python manage.py createsuperuser`
2. Run server:
  `python manage.py runserver`
3. Login the employee: go to <http://127.0.0.1:8000/user/login/>.
4. Create new customer: go to <http://127.0.0.1:8000/user/signup/> and fill in the required fields.
5. Create an account: go to <http://127.0.0.1:8000/account/create_account/>. Default balance = 100 USD, modify it if needed.
6. To check the account summary, go to <http://127.0.0.1:8000/account/1/>.
7. To transfer money, go to <http://127.0.0.1:8000/account/money_transfer/>, fill in `account_to` and `amount` and press PUT (double-check if `account_from` and `account_to` exist).
8. To see the transfer history list for all accounts, go to <http://127.0.0.1:8000/account/transfer_log/>.
9. To see the transfer history list for current account, go to <http://127.0.0.1:8000/account/transfer_log/1/>.
10. To logout, go to <http://127.0.0.1:8000/customer/logout/>.

Note: JWTAuthentication is applied, therefore all the requests must include a token in HEADER.
