# JSON integration

Use `--json` to export a single-date balance for scripts. The default remains human-readable text. `--json` and `--csv` are mutually exclusive.

```sh
python3 vesting.py --total 100 --start 2026-01-01 --end 2026-01-11 --as-of 2026-01-06 --tge-percent 20 --json
```

```json
{"date": "2026-01-06", "unlocked": "60", "locked": "40"}
```

`date` is an ISO calendar date. `unlocked` and `locked` are decimal strings, deliberately avoiding conversion to binary floating-point JSON numbers. Convert them with `decimal.Decimal` in Python, or an equivalent decimal library in another language. Values may use exponent notation and retain the calculator precision described in [README](README.md).

```python
import json
import subprocess
import sys
from decimal import Decimal

result = subprocess.run(
    [sys.executable, "vesting.py", "--total", "0.1",
     "--start", "2026-01-01", "--end", "2026-01-11",
     "--as-of", "2026-01-06", "--json"],
    check=True, capture_output=True, text=True,
)
balance = json.loads(result.stdout)
assert Decimal(balance["unlocked"]) == Decimal("0.05")
```

Check the process exit code before decoding stdout. Invalid inputs and conflicting output modes exit with code 2; diagnostics are written to stderr. Pass `--as-of` explicitly for reproducible results.
