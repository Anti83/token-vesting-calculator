import csv
import io
import subprocess
import sys
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path
from vesting import unlocked

class TgeTests(unittest.TestCase):
    def setUp(self):
        self.start = date(2026, 1, 1)
        self.end = date(2026, 1, 11)

    def test_tge_and_linear_remainder(self):
        for day, expected in [(date(2025, 12, 31), 0), (self.start, 20), (date(2026, 1, 6), 60), (self.end, 100)]:
            with self.subTest(day=day):
                self.assertEqual(unlocked(100, self.start, self.end, day, tge_percent=20), expected)

    def test_cliff_does_not_lock_initial_distribution(self):
        cliff = date(2026, 1, 6)
        self.assertEqual(unlocked(100, self.start, self.end, date(2026, 1, 5), cliff, 20), 20)
        self.assertEqual(unlocked(100, self.start, self.end, cliff, cliff, 20), 60)

    def test_full_tge_and_fractional_percent(self):
        self.assertEqual(unlocked(100, self.start, self.end, self.start, tge_percent=100), 100)
        self.assertEqual(unlocked(100, self.start, self.end, self.start, tge_percent='12.5'), Decimal('12.5'))

    def test_invalid_percentage(self):
        for value in ['-1', '101', 'NaN', 'Infinity']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                unlocked(100, self.start, self.end, self.start, tge_percent=value)

    def test_cli_csv_includes_tge(self):
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('vesting.py')), '--total', '100', '--start', '2026-01-01', '--end', '2026-01-11', '--tge-percent', '20', '--csv'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(io.StringIO(result.stdout)))
        self.assertEqual(len(rows), 11)
        self.assertEqual(Decimal(rows[0]['unlocked']), 20)
        self.assertEqual(Decimal(rows[5]['unlocked']), 60)
        self.assertEqual(Decimal(rows[-1]['unlocked']), 100)

if __name__ == '__main__':
    unittest.main()
