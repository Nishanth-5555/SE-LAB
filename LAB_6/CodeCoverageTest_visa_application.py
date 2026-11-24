"""Lab 6 - Code (line) coverage tests for visa_application.py.

Goal: execute every line of visa_application.py at least once (>= 90% line coverage).
"""
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ---------------- visa_fee ----------------

def test_within_included_entries():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_unknown_visa_type_raises():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("work", 1, "normal", "B")


def test_negative_entries_raises():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_group_a_gets_one_extra_included_entry():
    # tourist includes 1 entry, group A adds 1 -> 2 entries are free
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_normal_speed_extra_entries():
    # tourist: 1 included, 3 entries -> 2 extra at 40
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_express_speed_extra_entries():
    # business: 3 included, 5 entries -> 2 extra at 100
    assert visa_fee("business", 5, "express", "B") == 200


def test_more_than_five_extra_express():
    # tourist: 1 included, 8 entries -> 7 extra at 100 + 20 + 10 = 130
    assert visa_fee("tourist", 8, "express", "B") == 910


# ---------------- documents_complete ----------------

def test_documents_complete():
    assert documents_complete(3, 2, False) is True


def test_renewal_needs_one_form():
    assert documents_complete(1, 0, True) is True


def test_too_few_photos():
    assert documents_complete(3, 1, False) is False


# ---------------- application_status ----------------

def test_status_open_normal():
    # normal cutoff 30
    assert application_status(40, False, False) == "open"


def test_status_closing_express():
    # express cutoff 10 -> 5 is within the closing window (>= -5)
    assert application_status(5, True, False) == "closing"


def test_status_closed_peak_season():
    # normal + peak: cutoff 45, closing window from 30 -> 10 is closed
    assert application_status(10, False, True) == "closed"
