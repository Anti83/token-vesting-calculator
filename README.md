# Token Vesting Calculator

[![Tests](https://github.com/Anti83/token-vesting-calculator/actions/workflows/tests.yml/badge.svg)](https://github.com/Anti83/token-vesting-calculator/actions/workflows/tests.yml)

An offline Python 3.10+ tool for reviewing linear token unlock schedules. No dependencies, RPC calls, wallet connection, or credentials.

## Quick start

```sh
git clone https://github.com/Anti83/token-vesting-calculator.git
cd token-vesting-calculator
python3 vesting.py --total 100 --start 2026-01-01 --end 2026-01-11 --as-of 2026-01-06
```

Expected output:

```text
Unlocked: 50
Locked: 50
```

## CLI options

| Option | Meaning |
| --- | --- |
| `--total` | Required finite, nonnegative allocation; decimal values accepted |
| `--start` | Required ISO date, zero unlocked |
| `--end` | Required ISO date after start, full allocation unlocked |
| `--cliff` | Optional ISO date inside the schedule; accrued tokens unlock on this date |
| `--as-of` | Calculation date; defaults to the machine's local date |
| `--csv` | Export daily balances to stdout, including start and end |

For a schedule with a cliff and for a CSV export:

```sh
python3 vesting.py --total 1000000 --start 2026-01-01 --end 2027-01-01 --cliff 2026-04-01 --as-of 2026-10-01
python3 vesting.py --total 1000000 --start 2026-01-01 --end 2027-01-01 --csv > schedule.csv
```

## Schedule semantics and limits

- Linear accrual uses actual elapsed calendar days, including leap days.
- Before the cliff nothing is unlocked; at the cliff the accrued balance becomes available immediately.
- Dates have calendar-day resolution, without time zones or intraday unlocks. Pass `--as-of` for reproducible calculations.
- Decimal arithmetic avoids binary floating-point errors. Recurring fractions use Python's default 28-digit decimal precision. Values are not rounded to on-chain token decimals.
- CSV intervals are limited to 36,600 days. Longer schedules still support a single-date calculation. Invalid arguments exit with code 2.

This models a continuous linear schedule. It does not model monthly installments, TGE allocations, revocable grants, or a specific smart contract. Verify actual project terms before relying on the result. CSV output is an analytical estimate, not transaction instructions.

## Development

```sh
python3 -m unittest -v
```

Eight tests cover boundaries, cliff catch-up, fractional allocations, invalid schedules, oversized CSV output, date.max and malformed CLI allocations. GitHub Actions runs tests on pushes and pull requests.

For bug reports include the exact command, Python version, expected result and actual result. Do not attach private keys, seed phrases or credentials.
