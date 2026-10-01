import unittest
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


if __name__ == '__main__':
    unittest.main()
