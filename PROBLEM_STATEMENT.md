# 🚀 Space Explorer — Problem Statement

**Difficulty**: Beginner  
**Estimated time**: 2–4 hours  
**Language**: Python 3.8+

---

## Background

You've been hired as a junior developer at **AstroBase**, a small space data startup.
Your first task is to build a command-line tool that lets users explore our solar system
and fetch live space data from NASA's free public API.

This project will give you hands-on experience with three skills every Python developer
needs: reading config files, calling APIs, and handling user input.

---

## What You Need to Build

Create a file called `space_explorer.py` alongside a `config.yaml` file.

---

## Requirements

### R1 — Load configuration from a YAML file

Your program must read a file called `config.yaml` at startup.

The YAML file must contain:

```yaml
app:
  name: "Space Explorer"

nasa:
  apod_url: "https://api.nasa.gov/planetary/apod"
  api_key: "DEMO_KEY"

planets:
  - name: Earth
    distance_from_sun_km: 149600000
    moons: 1
    fun_fact: "Earth is the only known planet with life!"
  # ... more planets
```

If `config.yaml` does not exist, print a helpful error message and exit.

---

### R2 — Display an interactive menu

When the program starts, show a menu like this:

```
What would you like to do?

[1]  Explore a planet
[2]  Get NASA Astronomy Picture of the Day
[3]  List all planets
[q]  Quit
```

The menu must keep showing after each action until the user types `q`.

---

### R3 — Planet explorer (option 1)

When the user picks option `1`:
- Ask them to type a planet name
- Look up that planet in the data loaded from `config.yaml`
- Print the planet's name, distance from the sun, number of moons, and fun fact
- If the planet is not found, print a helpful message (do NOT crash)
- The search must be **case-insensitive** (`earth`, `Earth`, `EARTH` all work)

---

### R4 — List all planets (option 3)

When the user picks option `3`:
- Print a numbered list of all planet names from the config

---

### R5 — NASA API call (option 2)

When the user picks option `2`:
- Make an HTTP GET request to: `https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY`
- Parse the JSON response
- Print the **title**, **date**, and first 300 characters of the **explanation**
- Also print the **url** field from the response
- If the network is unavailable, print a friendly error message (do NOT crash)

The JSON response from NASA looks like this:

```json
{
  "title": "Some Space Thing",
  "date": "2024-01-15",
  "explanation": "A long description...",
  "url": "https://apod.nasa.gov/apod/image/...",
  "media_type": "image"
}
```

---

### R6 — Handle unknown input

If the user types anything other than `1`, `2`, `3`, or `q`, print a message like:
```
Unknown option. Please type 1, 2, 3, or q.
```

---

## Constraints

- Use only Python's **standard library** for HTTP requests (`urllib.request`)
- Use **PyYAML** for reading the config file (`pip install pyyaml`)
- Do **not** use `requests`, `httpx`, or any other third-party HTTP library
- All logic must be in **functions** — no bare code at the top level (except the `if __name__ == "__main__"` block)

---

## File Structure

```
space_explorer/
├── space_explorer.py    ← Your main program
├── config.yaml          ← Your config file
└── test_space_explorer.py  ← Test suite (provided — do not modify)
```

---

## Hints

- `yaml.safe_load(file)` turns a YAML file into a Python dictionary
- `urllib.request.urlopen(url)` makes an HTTP GET request
- `json.loads(data)` turns a JSON string into a Python dictionary
- `str.lower()` makes a string lowercase for case-insensitive comparison
- Wrap network calls in `try/except urllib.error.URLError` to handle failures
- Use `if __name__ == "__main__":` as your entry point

---

## Stretch Goals (optional, not tested)

Once your tests pass, try these challenges:

- 🟡 **Medium**: Add option `[4]` to fetch a specific date's APOD — ask the user for a date in `YYYY-MM-DD` format and add it as a query parameter
- 🟡 **Medium**: Add a `distance_from_earth_km` field to each planet in the config and display it
- 🔴 **Hard**: Save each APOD you fetch to a `history.json` file, and add option `[5]` to view your history

---

## How to Run the Tests

```bash
pip install pyyaml pytest
pytest test_space_explorer.py -v
```

All 15 tests should pass. Good luck, explorer! 🌟
