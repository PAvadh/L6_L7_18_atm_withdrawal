import pytest

from atm_withdrawal import withdraw, pin_check, note_breakup


def test_withdraw_rejects_unknown_account():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "student", True)


def test_withdraw_rejects_invalid_amounts():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 150, "savings", True)


def test_withdraw_exceeds_daily_limit():
    assert withdraw(30000, 25100, "savings", True) == "limit exceeded"


def test_withdraw_external_bank_large_amount_insufficient_funds():
    # Executes the external-bank fee and the additional fee for amounts > 10,000.
    assert withdraw(10000, 11000, "current", False) == "insufficient funds"


def test_withdraw_own_bank_success():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_pin_check_all_return_statements():
    assert pin_check(1111, 1234, 3) == "card blocked"
    assert pin_check(1234, 1234, 0) == "ok"
    assert pin_check(1111, 1234, 2) == "card blocked"
    assert pin_check(1111, 1234, 0) == "retry"


def test_note_breakup_rejects_non_hundred_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(250)


def test_note_breakup_large_remainder():
    assert note_breakup(900) == (1, 2, 0)


def test_note_breakup_small_remainder():
    # Executes the else block when the remainder is less than 200.
    assert note_breakup(600) == (1, 0, 1)
