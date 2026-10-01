# Token Vesting Calculator

[![Tests](https://github.com/Anti83/token-vesting-calculator/actions/workflows/tests.yml/badge.svg)](https://github.com/Anti83/token-vesting-calculator/actions/workflows/tests.yml)

An offline Python 3.10+ tool for reviewing token unlock schedules. No dependencies, RPC calls, wallet connection, or credentials.

## Quick start

```sh
git clone https://github.com/Anti83/token-vesting-calculator.git
cd token-vesting-calculator
python3 vesting.py --total 100 --start 2026-01-01 --end 2026-01-11 --as-of 2026-01-06
```

Expected: 50 unlocked, 50 locked.

## Initial TGE distribution

```sh
python3 vesting.py --total 100 --start 2026-01-01 --end 2026-01-11 --tge-percent 20 --as-of 2026-01-06
```

20 tokens unlock on the start date. The remaining 80 vest linearly, so halfway through the schedule 60 are unlocked and 40 locked. A cliff applies to the remaining allocation; the TGE portion stays available from the start date. At the cliff, accrued remainder catches up.

## CLI options

| Option | Meaning |
| --- | --- |
| `--total` | Required finite, nonnegative allocation; decimal values accepted |
| `--start` | Required ISO date; initial TGE portion becomes available |
| `--end` | Required ISO date after start; full allocation unlocked |
| `--tge-percent` | Percentage initially unlocked, 0–100; default 0 |
| `--cliff` | Optional ISO date inside the schedule; accrued remainder unlocks here |
| `--as-of` | Calculation date; defaults to the machine local date |
| `--csv` | Export daily balances, including start and end |

```sh
python3 vesting.py --total 1000000 --start 2026-01-01 --end 2027-01-01 --cliff 2026-04-01 --tge-percent 10 --csv > schedule.csv
```

## Schedule semantics and limits

- Before the start date nothing is unlocked.
- Linear accrual uses actual elapsed calendar days, including leap days.
- Dates have calendar-day resolution without intraday unlocks. Pass `--as-of` for reproducible results.
- Decimal arithmetic avoids binary floating-point errors. Recurring fractions use Python default 28-digit precision; values are not rounded to on-chain token decimals.
- CSV intervals are limited to 36,600 days. Longer schedules still support a single-date calculation. Invalid arguments exit with code 2.

This models continuous linear vesting with an optional initial allocation and cliff. It does not model monthly installments, revocable grants, or a specific smart contract. Verify actual project terms. CSV output is an analytical estimate.

## Development

```sh
python3 -m unittest -v
```

Tests cover boundaries, cliff catch-up, fractional allocations, invalid schedules, oversized CSV output, the maximum calendar date, malformed CLI inputs, TGE percentages, and daily CSV balances. GitHub Actions runs tests on pushes and pull requests.

For bug reports include the exact command, Python version, expected result, and actual result. Do not attach private keys, seed phrases, or credentials.
