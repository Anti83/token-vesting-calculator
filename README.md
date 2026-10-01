# Token Vesting Calculator

A small offline Python 3.10+ tool for reviewing linear token unlock schedules. No dependencies, RPC calls, wallet connection, or credentials.

## Usage

```sh
python3 vesting.py --total 1000000 --start 2026-01-01 --end 2027-01-01 --cliff 2026-04-01 --as-of 2026-10-01
python3 vesting.py --total 1000000 --start 2026-01-01 --end 2027-01-01 --csv > schedule.csv
python3 -m unittest -v
```

## Schedule semantics

- Start date: zero unlocked. End date: full allocation unlocked.
- Linear accrual uses actual elapsed calendar days, including leap days.
- Before the optional cliff nothing is unlocked; on the cliff date accrued tokens become available immediately.
- Dates are interpreted as UTC calendar dates, without intraday resolution. Pass `--as-of` explicitly for reproducible results; its default is the machine's local date.
- Decimal arithmetic avoids binary floating-point errors. Recurring fractions use Python's default 28-digit decimal precision. Outputs are not rounded to a token's on-chain decimals.

This models a simple continuous schedule, not monthly installments, TGE allocations, revocable grants, or a specific smart contract. Verify the project's actual terms before relying on the result. The CSV is an analytical estimate, not transaction instructions.

## Development

Tests cover schedule boundaries, cliff catch-up, fractional allocations, and invalid input. Contributions with reproducible examples are welcome.
