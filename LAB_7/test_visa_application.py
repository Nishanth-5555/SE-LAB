"""Lab 7 - Hypothesis fuzz tests for visa_application.py.

Two kinds of properties per function:
  1. *No crash*: for ANY text (or None) the function must not raise - it should
     return a result for valid input and None for invalid input.
  2. *Correctness*: for well-formed generated input the result must be right.
"""
import math

from hypothesis import given, settings, strategies as st

from visa_application import parse_application, processing_average, payable_fee

VISA_TYPES = ["tourist", "business", "student"]

# Fuzz inputs: random unicode text, None, and "nearly valid" strings built from
# the characters the parsers care about (digits, separators, signs, spaces, nan/inf ...).
nearly_valid = st.text(alphabet="0123456789:,|.-+ eEnaifNIabcxyz\t", max_size=30)
fuzz_input = st.text() | st.none() | nearly_valid


# ---------------- parse_application ----------------

@settings(max_examples=500)
@given(fuzz_input)
def test_parse_application_no_crash(s):
    try:
        result = parse_application(s)
    except Exception as e:  # noqa: BLE001 - any exception is a fuzzing failure
        assert False, f"parse_application crashed on {s!r} with: {e!r}"
    assert result is None or (isinstance(result, tuple) and len(result) == 2)


@given(st.sampled_from(VISA_TYPES), st.integers(min_value=0, max_value=10**6),
       st.sampled_from(["", " ", "  "]))
def test_parse_application_valid(visa, entries, pad):
    text = f"{pad}{visa}{pad}:{pad}{entries}{pad}"
    assert parse_application(text) == (visa.title(), entries)


# ---------------- processing_average ----------------

@settings(max_examples=500)
@given(fuzz_input)
def test_processing_average_no_crash(s):
    try:
        result = processing_average(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"processing_average crashed on {s!r} with: {e!r}"
    assert result is None or isinstance(result, int)


@given(st.lists(st.integers(min_value=0, max_value=10**4), min_size=1, max_size=20))
def test_processing_average_valid(days):
    result = processing_average(",".join(map(str, days)))
    assert result == sum(days) // len(days)
    assert min(days) <= result <= max(days)


# ---------------- payable_fee ----------------

@settings(max_examples=500)
@given(fuzz_input)
def test_payable_fee_no_crash(s):
    try:
        result = payable_fee(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"payable_fee crashed on {s!r} with: {e!r}"
    # a fee must never be negative, NaN or infinite
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.floats(min_value=0, max_value=1e7), st.floats(min_value=0, max_value=1e7))
def test_payable_fee_valid(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    expected = max(fee * 1.18 - discount, 0)
    assert result is not None and result >= 0
    assert math.isclose(result, expected, abs_tol=0.01)
