from app.calculations import add,subtract, multiply, divide, BankAccount,InsufficientFunds
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def initial_bank_account():
    return BankAccount(2000)

@pytest.mark.parametrize("num1,num2,expected", [(3,4,7),(4,8,12),(9,1,10),(2,6,8)])
def test_add(num1,num2,expected):
    assert add(num1,num2) == expected
def test_subtract():
    assert subtract(9,7) == 2
def test_multiply():
    assert multiply(7,9)== 63
def test_divide():
    assert divide(8,2) == 4

def test_bank_set_initial_amount(initial_bank_account):
    #bank_account= BankAccount(50)
    assert initial_bank_account.balance == 2000

def test_default_amount(zero_bank_account):
    #bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw(initial_bank_account):
    #bank_balance = BankAccount(2000)
    initial_bank_account.withdraw(1500)
    assert initial_bank_account.balance == 500
def test_deposit(initial_bank_account):
    #bank_balance = BankAccount(2000)
    initial_bank_account.deposit(79)
    assert initial_bank_account.balance == 2079

def test_interest(initial_bank_account):
    #bank_balance = BankAccount(2000)
    initial_bank_account.interest()
    assert initial_bank_account.balance == 2200

@pytest.mark.parametrize("deposited,withdrew, expected", [(2000,500,1500), (4000,1000,3000), (120000,29000,91000)])
def test_transactions(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected      

def test_insufficient_funds(initial_bank_account):
    with pytest.raises(InsufficientFunds):
        initial_bank_account.withdraw(3000)
        assert initial_bank_account.balance == -2000
