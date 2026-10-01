"""Offline linear vesting calculator. All dates are UTC calendar dates."""
import argparse
import csv
import sys
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation


def unlocked(total, start, end, as_of, cliff=None):
    total = Decimal(str(total))
    if not total.is_finite() or total < 0:
        raise ValueError('total must be finite and nonnegative')
    if end <= start:
        raise ValueError('end must be after start')
    if cliff is not None and not start <= cliff <= end:
        raise ValueError('cliff must fall between start and end')
    if as_of < start or (cliff is not None and as_of < cliff):
        return Decimal(0)
    if as_of >= end:
        return total
    return total * Decimal((as_of - start).days) / Decimal((end - start).days)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--total', required=True, type=Decimal)
    parser.add_argument('--start', required=True, type=date.fromisoformat)
    parser.add_argument('--end', required=True, type=date.fromisoformat)
    parser.add_argument('--cliff', type=date.fromisoformat)
    parser.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    parser.add_argument('--csv', action='store_true', help='Export every daily balance to stdout')
    args = parser.parse_args()
    try:
        amount = unlocked(args.total, args.start, args.end, args.as_of, args.cliff)
        if args.csv:
            writer = csv.writer(sys.stdout)
            writer.writerow(['date', 'unlocked', 'locked'])
            day = args.start
            while day <= args.end:
                value = unlocked(args.total, args.start, args.end, day, args.cliff)
                writer.writerow([day.isoformat(), value, args.total - value])
                day += timedelta(days=1)
        else:
            print(f'Unlocked: {amount}\nLocked: {args.total - amount}')
    except (ValueError, InvalidOperation) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
