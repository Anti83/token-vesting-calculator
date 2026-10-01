import json
import subprocess
import sys
import unittest
from pathlib import Path

class JsonTests(unittest.TestCase):
    def run_cli(self, *extra):
        return subprocess.run([sys.executable, str(Path(__file__).with_name('vesting.py')),
            '--total', '100', '--start', '2026-01-01', '--end', '2026-01-11',
            '--as-of', '2026-01-06', *extra], capture_output=True, text=True)

    def test_tge_json_balance(self):
        result = self.run_cli('--tge-percent', '20', '--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {'date': '2026-01-06', 'unlocked': '60', 'locked': '40'})

    def test_fractional_values_are_strings(self):
        result = self.run_cli('--total', '0.1', '--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['unlocked'], '0.05')

    def test_output_modes_conflict_before_writing(self):
        result = self.run_cli('--json', '--csv')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertNotIn('Traceback', result.stderr)

if __name__ == '__main__':
    unittest.main()
