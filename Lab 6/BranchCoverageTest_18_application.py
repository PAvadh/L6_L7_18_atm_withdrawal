import pytest

from atm_withdrawal import withdraw, pin_check, note_breakup


# Withdrawal validation and daily-limit decisions
def test_withdraw_account_type_branches():
    assert withdraw(5000, 1000, "savings", True) == 4000
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "business", True)


def test_withdraw_amount_validation_branches():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, -100, "savings", True)  # amount <= 0
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 150, "savings", True)   # amount % 100 != 0
    assert withdraw(5000, 100, "savings", True) == 4900


def test_withdraw_daily_limit_branches():
    assert withdraw(30000, 25100, "savings", True) == "limit exceeded"
    assert withdraw(30000, 25000, "savings", True) == 5000


def test_withdraw_bank_fee_branches():
    assert withdraw(5000, 1000, "savings", True) == 4000
    assert withdraw(5000, 1000, "savings", False) == 3980
    assert withdraw(20000, 11000, "current", False) == 8970


def test_withdraw_funds_branches():
    assert withdraw(1000, 1000, "savings", True) == 0
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


# PIN check: blocked, correct PIN, final wrong attempt, and retry
def test_pin_check_branches():
    assert pin_check(1111, 1234, 3) == "card blocked"
    assert pin_check(1234, 1234, 0) == "ok"
    assert pin_check(1111, 1234, 2) == "card blocked"
    assert pin_check(1111, 1234, 1) == "retry"


# Note breakup: invalid amount and both remainder outcomes
def test_note_breakup_branches():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(250)
    assert note_breakup(900) == (1, 2, 0)   # remainder 400 >= 200
    assert note_breakup(600) == (1, 0, 1)   # remainder 100 < 200
