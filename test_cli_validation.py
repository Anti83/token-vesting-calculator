import subprocess
import sys
import unittest
from pathlib import Path


class InputValidationTests(unittest.TestCase):
    def test_invalid_totals_produce_usage_errors(self):
        for total in ['invalid', 'NaN', 'Infinity', '-1']:
            with self.subTest(total=total):
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).with_name('vesting.py')),
                     '--total', total, '--start', '2026-01-01', '--end', '2027-01-01'],
                    capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')
                self.assertIn('error:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
