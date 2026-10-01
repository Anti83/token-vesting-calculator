"""Offline linear vesting calculator. Dates use calendar-day resolution."""
import argparse
import csv
import sys
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation


def unlocked(total, start, end, as_of, cliff=None, tge_percent=0):
    total = Decimal(str(total))
    tge_percent = Decimal(str(tge_percent))
    if not total.is_finite() or total < 0:
        raise ValueError('total must be finite and nonnegative')
    if end <= start:
        raise ValueError('end must be after start')
    if cliff is not None and not start <= cliff <= end:
        raise ValueError('cliff must fall between start and end')
    if not tge_percent.is_finite() or not 0 <= tge_percent <= 100:
        raise ValueError('TGE percentage must be between 0 and 100')
    if as_of < start:
        return Decimal(0)
    initial = total * tge_percent / Decimal(100)
    if cliff is not None and as_of < cliff:
        return initial
    if as_of >= end:
        return total
    return initial + (total - initial) * Decimal((as_of - start).days) / Decimal((end - start).days)


def parse_total(value):
    try:
        amount = Decimal(value)
    except InvalidOperation:
        raise argparse.ArgumentTypeError('total must be a decimal number') from None
    if not amount.is_finite() or amount < 0:
        raise argparse.ArgumentTypeError('total must be finite and nonnegative')
    return amount


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--total', required=True, type=parse_total)
    parser.add_argument('--start', required=True, type=date.fromisoformat)
    parser.add_argument('--end', required=True, type=date.fromisoformat)
    parser.add_argument('--cliff', type=date.fromisoformat)
    parser.add_argument('--tge-percent', type=parse_total, default=Decimal(0),
                        help='Percentage unlocked at start; the remainder vests linearly')
    parser.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    parser.add_argument('--csv', action='store_true', help='Export every daily balance to stdout')
    args = parser.parse_args()
    try:
        amount = unlocked(args.total, args.start, args.end, args.as_of, args.cliff, args.tge_percent)
        if args.csv:
            if (args.end - args.start).days > 36600:
                raise ValueError('CSV schedules must not exceed 36,600 days')
            writer = csv.writer(sys.stdout)
            writer.writerow(['date', 'unlocked', 'locked'])
            day = args.start
            while day <= args.end:
                value = unlocked(args.total, args.start, args.end, day, args.cliff, args.tge_percent)
                writer.writerow([day.isoformat(), value, args.total - value])
                if day == args.end:
                    break
                day += timedelta(days=1)
        else:
            print(f'Unlocked: {amount}\nLocked: {args.total - amount}')
    except (ValueError, InvalidOperation) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
