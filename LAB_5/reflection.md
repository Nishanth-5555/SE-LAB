# Lab 5: Reflection

**Name:** Nishanth N Aralaguppe  **SRN:** PES1UG24AM179

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the mechanical ones: the unused `math` import, the unused `lab_fee` variable, `== None` → `is None`, the
missing final newline, and the long lines. Each has exactly one correct fix and nothing else depends on it. Renaming the
camelCase functions was also easy because they are only called from `main()`.

The hardest was the `eval()` in `calculateScholarshipTuition` (Bandit B307). Deleting `eval` was not enough, because the
function's interface was built around passing code as a string (`"base_fee * 0.75"`). I had to redesign it to take a
numeric `discount_rate`, validate the range, and update the caller while keeping the same result (450.0). The global
`total_tuition` (W0603) also needed a design decision rather than a one-line change. The hardest problem of all was
one no tool reported: `dropCourse` reopened a full course nobody had left, which only showed up as a wrong
"Open courses: 3" in the program's output.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Partly. Bandit's **B105** flags `registrar_auth_token = "..."` only because the variable name contains "token"; it
would flag a harmless string assigned to a similarly named variable too, and it does not notice that the bigger problem
was that the token was printed. In this file the finding was real, but the rule is a name-based heuristic.

A clearer case of a misleading report is **F841 / W0612 on `base_fee`**. Both Flake8 and Pylint said `base_fee` was
unused, but it was used, inside the string passed to `eval`. The tools cannot see into a string, so "unused variable"
is technically wrong. Simply deleting the variable would have made the `eval` raise `NameError`. The report pointed at
the right line for the wrong reason, and the real problem was the `eval`.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** run Flake8 and Pylint inside the editor (VS Code extensions) so problems are fixed while typing, and add
  a `pre-commit` hook that runs Flake8, Pylint and Bandit on staged files, so badly formatted or insecure code never
  reaches a commit.
- **In CI:** a GitHub Actions job on every push and pull request that runs all three tools and fails the build if
  Bandit reports any Medium/High issue, Flake8 reports anything, or the Pylint score drops below a threshold (e.g. 9.5).
- **Configuration:** keep the rules in `pyproject.toml` / `.flake8` so the whole team uses the same settings. Use
  `# nosec` or `# pylint: disable=...` only with a written reason, so ignored warnings stay visible in code review.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** Bandit went from 6 issues (2 High, 1 Medium) to 0. The program can no longer run arbitrary code through
  `eval`, run shell commands through a filename, or leak the registrar token on screen. OTPs and student hashes use
  secure algorithms.
- **Robustness:** errors are no longer swallowed by a bare `except`. Audit entries are no longer shared between calls
  through the mutable default list. The roster file is always closed, and drops can no longer create seats out of
  nothing.
- **Readability:** Pylint went from 4.00 to 10.00 and Flake8 from 12 warnings to 0. Every function has a docstring and a
  PEP 8 name, the if/else chains became single expressions, and the code is easier to scan.
- **Testability:** with the `if __name__ == "__main__"` guard the module can be imported without side effects, which made
  it possible to check the fixed behaviour directly (no double enrollment, no double drop, discount validation).
