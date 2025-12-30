import argparse
import random
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd


def _rand_choice(rng: random.Random, items):
    return items[rng.randrange(0, len(items))]


def _make_amount(rng: random.Random) -> float:
    # Realistic-ish transaction amounts
    base = rng.choice([12.34, 25.00, 48.19, 75.55, 120.00, 249.99, 500.00])
    jitter = rng.uniform(-2.0, 2.0)
    amt = max(1.0, base + jitter)
    # Round to 2 decimals as typical currency
    return round(amt, 2)


def generate_synthetic_exports(
    n: int = 60,
    seed: int = 42,
    start_date: str = "2025-11-01",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generates two CSV-like datasets:
      - ledger_export: internal ledger extract
      - bank_export: bank statement export
    Includes intentional issues: duplicates, missing values, formatting differences,
    partial mismatches, date drift, amount rounding differences.
    """
    rng = random.Random(seed)
    start = datetime.strptime(start_date, "%Y-%m-%d").date()

    vendors = [
        "Acme Supplies",
        "North Star Utilities",
        "Metro Transit",
        "OfficeHub",
        "CloudNine Hosting",
        "Paper & Co",
        "Catering Partners",
    ]
    categories = ["Supplies", "Utilities", "Transport", "Software", "Meals", "Other"]
    methods = ["ACH", "Card", "Wire"]

    rows_ledger = []
    rows_bank = []

    for i in range(n):
        txn_id = f"TXN-{100000 + i}"
        vendor = _rand_choice(rng, vendors)
        category = _rand_choice(rng, categories)
        method = _rand_choice(rng, methods)

        # Base date and amount (ledger)
        d0 = start + timedelta(days=rng.randrange(0, 25))
        amt0 = _make_amount(rng)

        memo = f"{vendor} {category} {method}"

        # Ledger row
        ledger_row = {
            "txn_id": txn_id,
            "post_date": d0.strftime("%Y-%m-%d"),
            "description": memo,
            "amount": f"{amt0:,.2f}",  # formatted number string
            "currency": "USD",
            "category": category,
        }
        rows_ledger.append(ledger_row)

        # Bank row derived from ledger but with drift/formatting issues
        drift_days = rng.choice([0, 0, 0, 1, -1, 2])  # mostly same day, sometimes drift
        d1 = d0 + timedelta(days=drift_days)

        # Rounding / formatting differences
        amt1 = amt0
        if rng.random() < 0.18:
            amt1 = round(amt0 + rng.choice([-0.01, 0.01, 0.02, -0.02]), 2)

        bank_desc = memo

        # Formatting differences: random extra spaces / case changes
        if rng.random() < 0.25:
            bank_desc = f"  {bank_desc.upper()}  "

        bank_row = {
            "bank_id": f"BANK-{200000 + i}",
            "date": d1.strftime("%m/%d/%Y"),  # different date format
            "details": bank_desc,
            "amount_usd": f"${amt1:,.2f}",  # currency symbol
        }
        rows_bank.append(bank_row)

    # Intentional issues
    # 1) Duplicate bank rows (simulate duplicate download or repeated posting)
    for _ in range(3):
        rows_bank.append(dict(_rand_choice(rng, rows_bank)))

    # 2) Missing values
    if rows_ledger:
        rows_ledger[rng.randrange(0, len(rows_ledger))]["description"] = ""
    if rows_bank:
        rows_bank[rng.randrange(0, len(rows_bank))]["details"] = ""

    # 3) Partial mismatch: bank amount changed more than rounding
    if rows_bank:
        j = rng.randrange(0, min(len(rows_bank), n))
        # Force a mismatch
        rows_bank[j]["amount_usd"] = "$999.99"

    # 4) Ledger txn_id missing (simulate bad export)
    if rows_ledger:
        rows_ledger[rng.randrange(0, len(rows_ledger))]["txn_id"] = ""

    ledger_df = pd.DataFrame(rows_ledger)
    bank_df = pd.DataFrame(rows_bank)

    return ledger_df, bank_df


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic ledger + bank CSVs.")
    parser.add_argument("--outdir", default="data/generated", help="Output directory")
    parser.add_argument("--n", type=int, default=60, help="Number of base transactions")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--start-date", default="2025-11-01", help="Start date YYYY-MM-DD")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    ledger_df, bank_df = generate_synthetic_exports(n=args.n, seed=args.seed, start_date=args.start_date)

    ledger_path = outdir / "ledger_export.csv"
    bank_path = outdir / "bank_export.csv"

    ledger_df.to_csv(ledger_path, index=False)
    bank_df.to_csv(bank_path, index=False)

    print(f"WROTE: {ledger_path}")
    print(f"WROTE: {bank_path}")
    print(f"ledger_rows={len(ledger_df)} bank_rows={len(bank_df)}")


if __name__ == "__main__":
    main()
