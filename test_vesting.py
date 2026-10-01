import unittest
import subprocess
import sys
from pathlib import Path
from datetime import date
from decimal import Decimal
from vesting import unlocked


class VestingTests(unittest.TestCase):
    def setUp(self):
        self.start = date(2026, 1, 1)
        self.end = date(2026, 1, 11)

    def test_boundaries(self):
        for day, expected in [(date(2025, 12, 31), 0), (self.start, 0),
                              (date(2026, 1, 6), 50), (self.end, 100),
                              (date(2027, 1, 1), 100)]:
            self.assertEqual(unlocked(100, self.start, self.end, day), expected)

    def test_cliff_catches_up(self):
        cliff = date(2026, 1, 6)
        self.assertEqual(unlocked(100, self.start, self.end, date(2026, 1, 5), cliff), 0)
        self.assertEqual(unlocked(100, self.start, self.end, cliff, cliff), 50)

    def test_fractional_total(self):
        self.assertEqual(unlocked('0.1', self.start, self.end, date(2026, 1, 6)), Decimal('0.05'))

    def test_invalid_schedule(self):
        for total in ['-1', 'NaN', 'Infinity']:
            with self.assertRaises(ValueError):
                unlocked(total, self.start, self.end, self.start)
        with self.assertRaises(ValueError):
            unlocked(100, self.start, self.start, self.start)
        with self.assertRaises(ValueError):
            unlocked(100, self.start, self.end, self.start, date(2027, 1, 1))


class CliTests(unittest.TestCase):
    def run_cli(self, start, end):
        return subprocess.run([sys.executable, str(Path(__file__).with_name('vesting.py')),
                               '--total', '100', '--start', start, '--end', end, '--csv'],
                              capture_output=True, text=True, timeout=10)

    def test_oversized_csv_has_no_partial_output(self):
        result = self.run_cli('1900-01-01', '2100-01-01')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('36,600', result.stderr)

    def test_century_is_supported(self):
        result = self.run_cli('2000-01-01', '2100-01-01')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[-1], '2100-01-01,100,0')

    def test_maximum_calendar_date(self):
        result = self.run_cli('9999-12-30', '9999-12-31')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[-1], '9999-12-31,100,0')


if __name__ == '__main__':
    unittest.main()
