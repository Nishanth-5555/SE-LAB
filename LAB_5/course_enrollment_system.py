"""Course enrollment system: enrolls students, handles drops, computes
scholarship tuition and exports the course roster."""
import hashlib
import os
import secrets

courses = {
    "CS101": {
        "title": "Data Structures", "seats": 3, "fee": 500.0,
        "is_closed": False, "enrolled": [],
    },
    "CS202": {
        "title": "Operating Systems", "seats": 0, "fee": 550.0,
        "is_closed": True, "enrolled": [],
    },
    "CS303": {
        "title": "Compiler Design", "seats": 4, "fee": 600.0,
        "is_closed": False, "enrolled": [],
    },
}

# Running total kept in a dict so functions can update it
# without needing a global statement
tuition_ledger = {"total": 0.0}


def enroll_student(course_id, student_name, credits_registered=3,
                   audit_trail=None):
    """Enroll a student in an open course and record the tuition.

    Returns True on success, False if the course is unknown or closed,
    or the student is already enrolled in it.
    """
    if audit_trail is None:
        audit_trail = []
    if course_id not in courses or courses[course_id]["is_closed"]:
        return False
    if student_name in courses[course_id]["enrolled"]:
        return False
    courses[course_id]["enrolled"].append(student_name)
    courses[course_id]["seats"] -= 1
    if courses[course_id]["seats"] <= 0:
        courses[course_id]["is_closed"] = True
    tuition_ledger["total"] += courses[course_id]["fee"]
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id, student_name):
    """Drop a student from a course and free their seat.

    Returns False if the course is unknown or the student was not enrolled,
    so a drop can no longer create seats out of nothing or reopen a course
    nobody has left.
    """
    if course_id not in courses:
        return False
    if student_name not in courses[course_id]["enrolled"]:
        return False
    courses[course_id]["enrolled"].remove(student_name)
    courses[course_id]["seats"] += 1
    courses[course_id]["is_closed"] = False
    return True


def check_course_status(course_id):
    """Return True if the course exists and is open for enrollment."""
    if courses.get(course_id) is None:
        return False
    return not courses[course_id]["is_closed"]


def calculate_scholarship_tuition(course_id, discount_rate):
    """Return the course fee after applying a discount rate between 0 and 1."""
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("discount_rate must be between 0 and 1")
    base_fee = courses[course_id]["fee"]
    return round(base_fee * (1 - discount_rate), 2)


def generate_student_hash(roll_no):
    """Return a SHA-256 hex digest of the student's roll number."""
    return hashlib.sha256(roll_no.encode()).hexdigest()


def generate_enrollment_otp():
    """Return a cryptographically secure 4-digit one-time password."""
    return 1000 + secrets.randbelow(9000)


def export_course_roster(filename="course_roster.txt"):
    """Write the current course catalogue to a text file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(courses))
    print("Course roster exported to:", filename)


def get_open_courses_summary(course_catalog):
    """Return how many courses in the catalogue are open."""
    return sum(
        1 for details in course_catalog.values() if not details["is_closed"]
    )


def main():
    """Run a short demonstration of the enrollment system."""
    registrar_auth_token = os.environ.get("REGISTRAR_AUTH_TOKEN")
    audit_trail = []
    print("Enrolled Kritika in CS101:",
          enroll_student("CS101", "Kritika", 4, audit_trail))
    print("Dropped Kritika from CS202:", drop_course("CS202", "Kritika"))
    print("Is CS101 open:", check_course_status("CS101"))
    print("Scholarship Fee:", calculate_scholarship_tuition("CS303", 0.25))
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())
    export_course_roster()
    print("Open courses:", get_open_courses_summary(courses))
    print("Total tuition collected:", tuition_ledger["total"])
    for entry in audit_trail:
        print("Audit:", entry)
    print("Registrar Token configured:", registrar_auth_token is not None)


if __name__ == "__main__":
    main()
