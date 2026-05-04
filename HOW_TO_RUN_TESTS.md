# 🧪 How to Run the Test Suite

## Prerequisites

You need Python 3.8+ installed. Check with:
```bash
python --version
```

---

## Step 1 — Set up your project folder

Make sure your folder looks like this before running tests:

```
space_explorer/
├── space_explorer.py        ← your solution (you write this)
├── config.yaml              ← your config file (you write this)
├── test_space_explorer.py   ← test suite (provided, do not modify)
├── PROBLEM_STATEMENT.md     ← requirements (provided)
└── HOW_TO_RUN_TESTS.md      ← this file
```

---

## Step 2 — Install dependencies

```bash
pip install pyyaml pytest
```

---

## Step 3 — Run the tests

From inside the `space_explorer/` folder:

```bash
pytest test_space_explorer.py -v
```

The `-v` flag means "verbose" — it shows each test name and whether it passed or failed.

---

## Understanding the output

### All passing ✅
```
test_space_explorer.py::TestLoadConfig::test_load_config_returns_dict        PASSED
test_space_explorer.py::TestLoadConfig::test_load_config_contains_planets     PASSED
...
19 passed in 0.10s
```

### Some failing ❌
```
test_space_explorer.py::TestShowPlanetInfo::test_planet_search_case_insensitive FAILED

FAILURES
━━━━━━━━
FAILED test_space_explorer.py::TestShowPlanetInfo::test_planet_search_case_insensitive
AssertionError: 'earth' should match 'Earth' regardless of case
```

The failure message tells you exactly what requirement isn't met yet.

---

## Running just one group of tests

```bash
# Only run the config-loading tests
pytest test_space_explorer.py::TestLoadConfig -v

# Only run the planet tests
pytest test_space_explorer.py::TestShowPlanetInfo -v

# Only run the NASA API tests
pytest test_space_explorer.py::TestFetchAstronomyPicture -v

# Only run the display tests
pytest test_space_explorer.py::TestShowApod -v
```

This is useful when you're working on one requirement at a time.

---

## Running a single test

```bash
pytest test_space_explorer.py::TestShowPlanetInfo::test_planet_search_case_insensitive -v
```

---

## Test groups and what they cover

| Group | # Tests | Requirement |
|---|---|---|
| `TestLoadConfig` | 4 | R1 — Reading the YAML config file |
| `TestShowPlanetInfo` | 7 | R3 — Planet explorer feature |
| `TestFetchAstronomyPicture` | 4 | R5 — NASA API call |
| `TestShowApod` | 4 | R5 — Displaying API results |

---

## Tips when a test fails

1. **Read the assertion message** — it describes exactly what went wrong
2. **Check the requirement** — find the matching R1–R5 in `PROBLEM_STATEMENT.md`
3. **Run just that one test** to get focused output
4. **Add a print statement** in your function to see what it's actually outputting
5. **The tests never make real network calls** — NASA API tests use a fake response, so no internet is needed

---

## Goal

All **19 tests passing** = your solution is complete. 🚀
