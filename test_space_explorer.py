"""
🧪 Space Explorer — Test Suite
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run with:  pytest test_space_explorer.py -v

DO NOT MODIFY THIS FILE.
These tests check your implementation of space_explorer.py.
All 15 tests must pass for a complete solution.
"""

import json
import os
import sys
import tempfile
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

# ── Make sure the student's file can be imported ─────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

try:
    import space_explorer
except ImportError:
    raise ImportError(
        "\n\n❌  Could not import space_explorer.py\n"
        "    Make sure space_explorer.py is in the same folder as this test file.\n"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Shared test data — used across multiple tests
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SAMPLE_CONFIG = {
    "app": {
        "name": "Space Explorer",
        "version": "1.0.0",
    },
    "nasa": {
        "apod_url": "https://api.nasa.gov/planetary/apod",
        "api_key": "DEMO_KEY",
    },
    "planets": [
        {
            "name": "Mercury",
            "distance_from_sun_km": 57900000,
            "moons": 0,
            "fun_fact": "A year on Mercury is just 88 Earth days!",
        },
        {
            "name": "Earth",
            "distance_from_sun_km": 149600000,
            "moons": 1,
            "fun_fact": "Earth is the only known planet with life!",
        },
        {
            "name": "Mars",
            "distance_from_sun_km": 227900000,
            "moons": 2,
            "fun_fact": "Mars has the tallest volcano in the solar system!",
        },
    ],
}

SAMPLE_APOD_RESPONSE = {
    "title": "The Pillars of Creation",
    "date": "2024-01-15",
    "explanation": "In this stunning image, the Eagle Nebula's famous pillars stretch across light years of space. " * 5,
    "url": "https://apod.nasa.gov/apod/image/pillars.jpg",
    "media_type": "image",
}

MINIMAL_YAML = """
app:
  name: Space Explorer
nasa:
  apod_url: https://api.nasa.gov/planetary/apod
  api_key: DEMO_KEY
planets:
  - name: Earth
    distance_from_sun_km: 149600000
    moons: 1
    fun_fact: Only planet with life!
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST GROUP 1 — YAML config loading (R1)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestLoadConfig(unittest.TestCase):

    def test_load_config_returns_dict(self):
        """R1 — load_config() must return a Python dictionary."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(MINIMAL_YAML)
            tmp_path = f.name
        try:
            result = space_explorer.load_config(tmp_path)
            self.assertIsInstance(result, dict,
                "load_config() should return a dict, not: " + type(result).__name__)
        finally:
            os.unlink(tmp_path)

    def test_load_config_contains_planets(self):
        """R1 — Loaded config must contain a 'planets' list."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(MINIMAL_YAML)
            tmp_path = f.name
        try:
            result = space_explorer.load_config(tmp_path)
            self.assertIn("planets", result,
                "config dict must have a 'planets' key")
            self.assertIsInstance(result["planets"], list,
                "'planets' must be a list")
        finally:
            os.unlink(tmp_path)

    def test_load_config_planet_has_required_fields(self):
        """R1 — Each planet in the config must have name, distance, moons, fun_fact."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(MINIMAL_YAML)
            tmp_path = f.name
        try:
            result = space_explorer.load_config(tmp_path)
            planet = result["planets"][0]
            for field in ["name", "distance_from_sun_km", "moons", "fun_fact"]:
                self.assertIn(field, planet,
                    f"Planet dict is missing required field: '{field}'")
        finally:
            os.unlink(tmp_path)

    def test_load_config_missing_file_raises_or_exits(self):
        """R1 — load_config() must not silently return None if file is missing."""
        with self.assertRaises((FileNotFoundError, SystemExit),
                msg="load_config() should raise FileNotFoundError or call sys.exit() when file is missing"):
            space_explorer.load_config("__nonexistent_file_xyz__.yaml")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST GROUP 2 — Planet info display (R3)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestShowPlanetInfo(unittest.TestCase):

    def _capture_output(self, planets, name):
        """Helper: run show_planet_info and capture what gets printed."""
        captured = StringIO()
        with patch("sys.stdout", captured):
            space_explorer.show_planet_info(planets, name)
        return captured.getvalue()

    def test_planet_found_shows_name(self):
        """R3 — Output must include the planet name."""
        output = self._capture_output(SAMPLE_CONFIG["planets"], "Earth")
        self.assertIn("Earth", output,
            "Planet name 'Earth' should appear in the output")

    def test_planet_found_shows_distance(self):
        """R3 — Output must include the distance from the sun."""
        output = self._capture_output(SAMPLE_CONFIG["planets"], "Earth")
        # Accept either raw number or formatted with commas
        self.assertTrue(
            "149600000" in output or "149,600,000" in output,
            "Distance from sun (149600000 or 149,600,000) should appear in output"
        )

    def test_planet_found_shows_moons(self):
        """R3 — Output must include the number of moons."""
        output = self._capture_output(SAMPLE_CONFIG["planets"], "Mars")
        self.assertIn("2", output,
            "Number of moons (2) should appear in output for Mars")

    def test_planet_found_shows_fun_fact(self):
        """R3 — Output must include the fun fact."""
        output = self._capture_output(SAMPLE_CONFIG["planets"], "Mercury")
        self.assertIn("88", output,
            "Fun fact about Mercury (mentions 88 days) should appear in output")

    def test_planet_search_case_insensitive(self):
        """R3 — Planet lookup must be case-insensitive."""
        for variant in ["earth", "EARTH", "eArTh"]:
            output = self._capture_output(SAMPLE_CONFIG["planets"], variant)
            self.assertIn("Earth", output,
                f"'{variant}' should match 'Earth' regardless of case")

    def test_planet_not_found_does_not_crash(self):
        """R3 — Searching for an unknown planet must not raise an exception."""
        try:
            self._capture_output(SAMPLE_CONFIG["planets"], "Pluto")
        except Exception as e:
            self.fail(f"show_planet_info() crashed on unknown planet: {e}")

    def test_planet_not_found_shows_helpful_message(self):
        """R3 — Searching for an unknown planet should print something (not stay silent)."""
        output = self._capture_output(SAMPLE_CONFIG["planets"], "Pluto")
        self.assertTrue(len(output.strip()) > 0,
            "Should print a helpful message when the planet is not found")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST GROUP 3 — NASA API call (R5)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestFetchAstronomyPicture(unittest.TestCase):

    def _make_mock_response(self, data: dict):
        """Helper: build a fake HTTP response that returns JSON data."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(data).encode("utf-8")
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        return mock_response

    def test_fetch_returns_dict_on_success(self):
        """R5 — fetch_astronomy_picture() must return a dict on success."""
        mock_resp = self._make_mock_response(SAMPLE_APOD_RESPONSE)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = space_explorer.fetch_astronomy_picture(
                "https://api.nasa.gov/planetary/apod", "DEMO_KEY"
            )
        self.assertIsInstance(result, dict,
            "fetch_astronomy_picture() should return a dict, not: " + str(type(result)))

    def test_fetch_returns_correct_title(self):
        """R5 — Returned dict must contain the correct title from JSON."""
        mock_resp = self._make_mock_response(SAMPLE_APOD_RESPONSE)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = space_explorer.fetch_astronomy_picture(
                "https://api.nasa.gov/planetary/apod", "DEMO_KEY"
            )
        self.assertEqual(result.get("title"), "The Pillars of Creation",
            "fetch_astronomy_picture() should parse and return the 'title' field")

    def test_fetch_handles_network_error_gracefully(self):
        """R5 — fetch_astronomy_picture() must not crash on network failure."""
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("no network")):
            try:
                result = space_explorer.fetch_astronomy_picture(
                    "https://api.nasa.gov/planetary/apod", "DEMO_KEY"
                )
                # Should return None (or any falsy value) rather than crashing
                self.assertFalse(result,
                    "Should return None or falsy value when network fails, not: " + str(result))
            except Exception as e:
                self.fail(f"fetch_astronomy_picture() should handle network errors gracefully, but raised: {e}")

    def test_fetch_uses_api_key_in_url(self):
        """R5 — The API key must be included in the request URL."""
        mock_resp = self._make_mock_response(SAMPLE_APOD_RESPONSE)
        captured_urls = []

        def fake_urlopen(url, **kwargs):
            captured_urls.append(url)
            return mock_resp

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            space_explorer.fetch_astronomy_picture(
                "https://api.nasa.gov/planetary/apod", "MY_TEST_KEY"
            )

        self.assertTrue(
            any("MY_TEST_KEY" in url for url in captured_urls),
            "The API key must be included in the URL passed to urlopen()"
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST GROUP 4 — APOD display (R5 continued)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestShowApod(unittest.TestCase):

    def _capture_apod_output(self, data):
        captured = StringIO()
        with patch("sys.stdout", captured):
            space_explorer.show_apod(data)
        return captured.getvalue()

    def test_show_apod_displays_title(self):
        """R5 — show_apod() must print the title."""
        output = self._capture_apod_output(SAMPLE_APOD_RESPONSE)
        self.assertIn("Pillars of Creation", output,
            "APOD title should appear in the output")

    def test_show_apod_displays_date(self):
        """R5 — show_apod() must print the date."""
        output = self._capture_apod_output(SAMPLE_APOD_RESPONSE)
        self.assertIn("2024-01-15", output,
            "APOD date should appear in the output")

    def test_show_apod_displays_url(self):
        """R5 — show_apod() must print the image URL."""
        output = self._capture_apod_output(SAMPLE_APOD_RESPONSE)
        self.assertIn("apod.nasa.gov", output,
            "APOD URL should appear in the output")

    def test_show_apod_handles_none_gracefully(self):
        """R5 — show_apod(None) must not crash (used when fetch fails)."""
        try:
            self._capture_apod_output(None)
        except Exception as e:
            self.fail(f"show_apod(None) should not crash, but raised: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Run summary
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("\n🧪 Running Space Explorer Test Suite...\n")
    unittest.main(verbosity=2)
