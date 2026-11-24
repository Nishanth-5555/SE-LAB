# Lab 5: Static Code Analysis — Issue Table

**Name:** Nishanth N Aralaguppe  **SRN:** PES1UG24AM179
**File:** `course_enrollment_system.py` (repo `L5_52_course_enrollment_system`)

| Metric | Before | After |
|---|---|---|
| Pylint score | 4.00/10 | **10.00/10** |
| Bandit issues | 6 (2 High, 1 Medium, 3 Low) | **0** |
| Flake8 issues | 12 | **0** |

Full tool output: `reports/before/` and `reports/after/`. Line numbers below refer to the **original** file.

## Issues found and fixed (high and medium severity first)

| # | Issue | Tool / code | Type | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|---------|-------------|--------------|
| 1 | Shell command injection | Bandit B605 (**High**) | Security | 63 | `os.system("echo ... " + filename)` passes the filename to a shell; a filename like `x; rm -rf ~` would run extra commands. | Removed the shell call; print the message with `print()`. |
| 2 | Weak hash (MD5) | Bandit B324 (**High**) | Security | 52 | `hashlib.md5` is cryptographically broken (collisions are cheap) and unsuitable for identifying students. | Use `hashlib.sha256`. |
| 3 | Arbitrary code execution via `eval` | Bandit B307 (**Medium**), Pylint W0123 | Security | 47 | `eval(discount_expr)` executes any Python string the caller passes, e.g. `__import__('os').system(...)`. | Replaced the expression string with a numeric `discount_rate` argument, validated to be between 0 and 1; fee = `base_fee * (1 - discount_rate)`. `main` now passes `0.25`, giving the same 450.0 result. |
| 4 | Hard-coded secret, printed to the console | Bandit B105 (Low) | Security | 75, 84 | Registrar token `"REGISTRAR_PORTAL_ROOT_SECRET_2026"` is stored in source code (and therefore in git history) and printed on every run. | Read it from the `REGISTRAR_AUTH_TOKEN` environment variable; only print whether a token is configured, never its value. |
| 5 | Insecure random for OTP | Bandit B311 (Low) | Security | 56 | `random.randint` is predictable (Mersenne Twister), so OTPs could be guessed. | Use `secrets.randbelow(9000) + 1000`. |
| 6 | Silent `try/except/pass` with bare `except` | Bandit B110, Pylint W0702, Flake8 E722 | Bug | 28–32 | Every error is swallowed, including `KeyboardInterrupt`; the caller never learns that the course did not exist. | Explicit `course_id not in courses` check; return `False` for an unknown course. |
| 7 | Mutable default argument | Pylint W0102 | Bug | 15 | `audit_trail=[]` is created once and shared by every call, so audit entries leak between unrelated enrollments. | Default to `None`; create a new list inside the function. |
| 8 | `global` statement | Pylint W0603, C0103 | Design | 12, 16 | `total_tuition` is modified through `global`, which hides state changes. | Keep the total in a module-level `tuition_ledger` dict that functions update in place; `main` now prints it. |
| 9 | File opened without `with` / encoding | Pylint R1732, W1514 | Bug | 60–62 | File handle leaks if `write` raises; encoding depends on the OS locale. | `with open(filename, "w", encoding="utf-8") as roster_file:` |
| 10 | Parameter shadows a global | Pylint W0621 | Maintainability | 66 | Parameter `courses` hides the module-level `courses` dict. | Renamed parameter to `course_catalog`. |
| 11 | Unused import / variables | Pylint W0611, W0612; Flake8 F401, F841 | Code quality | 4, 36, 46, 68 | `math` never used; `lab_fee` never used; `base_fee` only used inside the eval string; loop variable `cid` unused. | Removed `math` and `lab_fee`; `base_fee` is now used directly; iterate over `.values()`. |
| 12 | Comparison to `None` with `==` | Pylint C0121, Flake8 E711 | Style / bug | 37 | `== None` can be overridden by `__eq__`; identity check is the correct test. | `is None`. |
| 13 | Redundant if/else | Pylint R1703, R1705 | Readability | 39–42 | `if x: return True else: return False`. | `return not courses[course_id]["is_closed"]`. |
| 14 | Non-PEP 8 names | Pylint C0103 | Style | 15, 27, 35, 45, 51, 55, 59, 66 | camelCase function names. | Renamed to snake_case (`enroll_student`, `drop_course`, …). |
| 15 | Missing docstrings | Pylint C0114, C0116 | Documentation | whole file | No module or function docstrings. | Added a module docstring and one per function. |
| 16 | Old-style `%` formatting | Pylint C0209 | Style | 23 | `"..." % (...)` string formatting. | f-string. |
| 17 | Module-level call to `main()` | — (best practice) | Design | 87 | Importing the module (e.g. in tests) would run the whole program. | `if __name__ == "__main__": main()` |
| 18 | Lines too long | Flake8 E501, Pylint C0301 | Style | 7–9, 15, 23, 79 | Lines up to 135 characters (PEP 8 limit is 79). | Wrapped the course dict, function signature, f-string and generator expression. |
| 19 | No newline at end of file | Flake8 W292, Pylint C0304 | Style | 87 | File ends without a newline. | Added trailing newline. |

## Logic bug not reported by any tool

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 20 | Dropping a course creates seats and reopens full courses | Logic bug | 27–30, 77 | `dropCourse("CS202")` adds a seat and reopens CS202 even though nobody was enrolled in it. The program then reports **"Open courses: 3"** when CS202 is still full. Repeated drops can push the seat count above the real capacity. | Each course now keeps an `enrolled` list. `drop_course(course_id, student_name)` only frees a seat if that student is actually enrolled, and `enroll_student` refuses duplicate enrollments. The demo now correctly reports `Dropped Kritika from CS202: False` and `Open courses: 2`. |

## Commits

1. **Fix Bandit security issues**: issues 1–6
2. **Fix Pylint issues**: issues 7–17, Pylint 4.84 → 10.00
3. **Fix Flake8 style issues**: issues 18–19, Flake8 now reports nothing
4. **Fix drop_course logic bug**: issue 20
5. **Add after-fix reports, issue table and reflection**
