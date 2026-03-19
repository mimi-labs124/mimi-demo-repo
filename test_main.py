import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable


def run_cmd(*args):
    return subprocess.run(
        [PYTHON, "main.py", *args],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class TestMimiQuoteCli(unittest.TestCase):
    def test_stats_command_works(self):
        result = run_cmd("stats")
        self.assertEqual(result.returncode, 0)
        self.assertIn("金句庫統計", result.stdout)

    def test_list_command_shows_builtin_quotes(self):
        result = run_cmd("list")
        self.assertEqual(result.returncode, 0)
        self.assertIn("全部金句", result.stdout)
        self.assertIn("[builtin]", result.stdout)

    def test_search_command_finds_quote(self):
        result = run_cmd("search", "市場")
        self.assertEqual(result.returncode, 0)
        self.assertIn("搜尋結果", result.stdout)
        self.assertIn("市場", result.stdout)

    def test_export_command_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "quotes.txt"
            result = subprocess.run(
                [PYTHON, str(REPO_DIR / "main.py"), "export", str(output)],
                cwd=REPO_DIR,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0)
            self.assertTrue(output.exists())
            self.assertIn("市場", output.read_text(encoding="utf-8"))

    def test_add_command_persists_custom_quote(self):
        quotes_path = REPO_DIR / "quotes.json"
        original = quotes_path.read_text(encoding="utf-8")
        new_quote = "測試金句：深度開發要真的落地。"
        try:
            result = run_cmd("add", new_quote)
            self.assertEqual(result.returncode, 0)
            data = json.loads(quotes_path.read_text(encoding="utf-8"))
            self.assertIn(new_quote, data)
        finally:
            quotes_path.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
