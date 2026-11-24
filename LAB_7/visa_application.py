"""Visa application helpers - hardened against invalid input (Lab 7 fuzzing fixes).

Every public function returns None instead of raising when the input is invalid.
"""
import math

MAX_INT_DIGITS = 9  # reject absurdly long numbers (also avoids int() DoS on huge strings)


def _parse_non_negative_int(token):
    """Return token as an int >= 0, or None if it is not a plain non-negative integer."""
    token = token.strip()
    if not token.isascii() or not token.isdigit() or len(token) > MAX_INT_DIGITS:
        return None
    return int(token)


def _parse_non_negative_float(token):
    """Return token as a finite float >= 0, or None."""
    try:
        value = float(token.strip())
    except ValueError:
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return value


def parse_application(text):
    """'tourist:2' -> ('Tourist', 2). Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    visa = parts[0].strip()
    if not visa or not visa.replace(' ', '').isalpha():
        return None
    entries = _parse_non_negative_int(parts[1])
    if entries is None:
        return None
    return visa.title(), entries


def processing_average(days_csv):
    """'5,10,21' -> 12 (integer average). Returns None for invalid input."""
    if not isinstance(days_csv, str) or not days_csv.strip():
        return None
    values = []
    for token in days_csv.split(','):
        value = _parse_non_negative_int(token)
        if value is None:  # empty field, text, negative or too large
            return None
        values.append(value)
    return sum(values) // len(values)


def payable_fee(text):
    """'6000|500' -> fee incl. 18% tax minus discount, never below 0. None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    fee = _parse_non_negative_float(parts[0])
    discount = _parse_non_negative_float(parts[1])
    if fee is None or discount is None:
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):  # e.g. 1e308 * 1.18 overflows to inf
        return None
    return round(max(total, 0), 2)


def _show(label, result):
    if result is None:
        print(f"{label}: Invalid input, please check the format.")
    else:
        print(f"{label}:", result)


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    _show("Visa Type and Entries", parse_application(user_input))

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    _show("Average Processing Days", processing_average(user_input))

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    _show("Payable Fee", payable_fee(user_input))


if __name__ == "__main__":
    main()
