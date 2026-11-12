
import re
from hypothesis import given, strategies as st
from atm_withdrawal import notes_needed, mask_card, average_withdrawal


# 1. Fuzz testing: notes_needed()
@given(st.one_of(st.text(), st.none()))
def test_notes_needed_no_crash(s):
    try:
        result = notes_needed(s)
        assert isinstance(result, int)
        assert result >= 0
    except ValueError:
        pass


# 2. Fuzz testing: mask_card()
@given(st.one_of(st.text(), st.none()))
def test_mask_card_no_crash(s):
    try:
        result = mask_card(s)
        assert re.fullmatch(r"XXXX XXXX XXXX \d{4}", result)
    except ValueError:
        pass


# 3. Fuzz testing: average_withdrawal()
@given(st.one_of(st.text(), st.none()))
def test_average_withdrawal_no_crash(s):
    try:
        result = average_withdrawal(s)
        assert isinstance(result, int)
        assert result >= 0
    except ValueError:
        pass


# 4. Valid input testing: notes_needed()
@given(st.integers(min_value=1, max_value=10**12))
def test_notes_needed_valid(amount):
    assert notes_needed(str(amount)) == amount // 100


# 5. Valid input testing: mask_card()
@given(st.text(alphabet="0123456789", min_size=16, max_size=16))
def test_mask_card_valid(card):
    result = mask_card(card)
    assert result == "XXXX XXXX XXXX " + card[-4:]


# 6. Valid input testing: average_withdrawal()
@given(st.lists(st.integers(min_value=1, max_value=100000),
                min_size=1, max_size=20))
def test_average_withdrawal_valid(amounts):
    csv_input = ",".join(map(str, amounts))
    expected = sum(amounts) // len(amounts)
    assert average_withdrawal(csv_input) == expected
