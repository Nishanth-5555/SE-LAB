# L6_L7_52 — Visa Application

Lab 7: Fuzz Testing

## About

A small Python module that parses visa applications, averages processing times and works out the payable fee after a discount.

## Files

| File | Description |
|------|-------------|
| `visa_application.py` | The code under test |
| `test_visa_application.py` | Starter test file |

Refer to the lab handout for instructions.

---

## Lab 7 Submission (PES1UG24AM179)

| File | Description |
|------|-------------|
| `visa_application.py` | Fixed (hardened) application - returns `None` for invalid input instead of crashing |
| `test_visa_application.py` | Hypothesis fuzz tests (no-crash + correctness properties for all three functions) |
| `Lab7_FuzzTesting_Screenshots.pdf` | Screenshots: buggy run, failing tests, fixed run, passing tests |
| `screenshots/` | The same screenshots as PNG files |

Run:
```
pip install hypothesis pytest
python visa_application.py
python -m pytest test_visa_application.py
```
