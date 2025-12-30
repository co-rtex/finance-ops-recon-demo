import argparse
import json
from pathlib import Path

import pandas as pd


def main():
    p = argparse.ArgumentParser(description="Validate reconciliation outputs (light QA).")
    p.add_argument("--outdir", required=True)
    args = p.parse_args()

    out = Path(args.outdir)
    matched_path = out / "matched.csv"
    exceptions_path = out / "exceptions.csv"
    summary_path = out / "summary.json"

    errors = []

    for fp in [matched_path, exceptions_path, summary_path]:
        if not fp.exists():
            errors.append(f"missing_file:{fp}")

    if errors:
        print("FAIL")
        for e in errors:
            print(e)
        raise SystemExit(1)

    matched = pd.read_csv(matched_path)
    exceptions = pd.read_csv(exceptions_path)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    # Basic count checks
    if int(summary["counts"]["matched_rows"]) != int(len(matched)):
        errors.append("count_mismatch:matched_rows")

    if int(summary["counts"]["exception_rows"]) != int(len(exceptions)):
        errors.append("count_mismatch:exception_rows")

    # Total checks (matched totals should align closely)
    matched_ledger_total = float(matched["ledger_amount"].sum()) if len(matched) else 0.0
    matched_bank_total = float(matched["bank_amount"].sum()) if len(matched) else 0.0
    if abs(matched_ledger_total - float(summary["totals"]["matched_ledger_total"])) > 0.01:
        errors.append("total_mismatch:matched_ledger_total")

    if abs(matched_bank_total - float(summary["totals"]["matched_bank_total"])) > 0.01:
        errors.append("total_mismatch:matched_bank_total")

    # Column presence sanity
    required_cols = {"match_reason", "ledger_id", "bank_id", "amount_diff", "date_diff_days"}
    missing = required_cols - set(matched.columns)
    if missing:
        errors.append(f"missing_columns_in_matched:{sorted(list(missing))}")

    if errors:
        print("FAIL")
        for e in errors:
            print(e)
        raise SystemExit(1)

    print("PASS")
    print(f"matched_rows={len(matched)} exceptions_rows={len(exceptions)}")
    print(f"matched_ledger_total={matched_ledger_total:.2f} matched_bank_total={matched_bank_total:.2f}")


if __name__ == "__main__":
    main()
