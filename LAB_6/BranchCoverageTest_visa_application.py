"""Lab 6 - Branch coverage tests for visa_application.py.

Goal: take every decision (if / elif / else) both the True and the False way
(>= 90% branch coverage), including boundary values.
"""
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ---------------- visa_fee ----------------

@pytest.mark.parametrize("visa_type", ["work", "", "TOURIST"])
def test_unknown_visa_type_raises(visa_type):          # line 5: True
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee(visa_type, 1, "normal", "B")


def test_negative_entries_raises():                    # line 7: True
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_zero_entries_is_free():                       # line 7: False (boundary 0)
    assert visa_fee("tourist", 0, "normal", "B") == 0


def test_group_a_non_student_gets_bonus_entry():       # line 10: True
    assert visa_fee("business", 4, "normal", "A") == 0


def test_group_a_student_gets_no_bonus_entry():        # line 10: False (student)
    # student includes 2, no bonus for group A -> 3 entries = 1 extra at 40
    assert visa_fee("student", 3, "normal", "A") == 40


def test_other_group_gets_no_bonus_entry():            # line 10: False (group B)
    assert visa_fee("business", 4, "normal", "B") == 40


def test_exactly_included_entries_is_free():           # line 13: True (extra == 0)
    assert visa_fee("student", 2, "express", "B") == 0


def test_one_extra_entry_express():                    # line 13: False, line 15: True
    assert visa_fee("tourist", 2, "express", "B") == 100


def test_one_extra_entry_normal():                     # line 15: False (else)
    assert visa_fee("tourist", 2, "normal", "B") == 40


def test_exactly_five_extra_no_surcharge():            # line 19: False (boundary 5)
    assert visa_fee("tourist", 6, "normal", "B") == 5 * 40


def test_more_than_five_extra_express():               # line 19: True, line 21: True
    # 6 extra at 100 + 20 + 10
    assert visa_fee("tourist", 7, "express", "B") == 6 * 130


def test_more_than_five_extra_normal():                # line 19: True, line 21: False
    # student: 2 included, 9 entries -> 7 extra at 40 + 20
    assert visa_fee("student", 9, "normal", "B") == 7 * 60


# ---------------- documents_complete ----------------

def test_renewal_with_form():                          # line 27: True -> True
    assert documents_complete(1, 0, True) is True


def test_renewal_without_form():                       # line 27: True -> False
    assert documents_complete(0, 5, True) is False


def test_new_application_too_few_photos():             # line 29: True
    assert documents_complete(5, 1, False) is False


def test_new_application_complete():                   # line 29: False -> True
    assert documents_complete(3, 2, False) is True


def test_new_application_too_few_forms():              # line 29: False -> False
    assert documents_complete(2, 2, False) is False


# ---------------- application_status ----------------

def test_express_open_at_cutoff():                     # line 35: True, 39: False, 41: True
    assert application_status(10, True, False) == "open"


def test_express_closing():                            # line 41: False, 43: True
    assert application_status(9, True, False) == "closing"


def test_express_peak_closed():                        # line 39: True, 43: False
    # express + peak: cutoff 25, closing from 10 -> 9 is closed
    assert application_status(9, True, True) == "closed"


def test_normal_open():                                # line 35: False (else)
    assert application_status(30, False, False) == "open"


def test_normal_closing_boundary():                    # closing window lower edge
    assert application_status(15, False, False) == "closing"


def test_normal_closed():
    assert application_status(14, False, False) == "closed"


def test_normal_peak_open():
    assert application_status(45, False, True) == "open"
