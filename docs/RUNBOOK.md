# RUNBOOK — Finance Ops Reconciliation Demo (Synthetic Data)
## Purpose
Reconcile a synthetic “ledger export” CSV against a synthetic “bank export” CSV and produce:
- matched transactions (with match reason)
- exceptions requiring human review
- summary metrics for auditability
- an Excel report for finance operations review
## Inputs (expected columns)
Ledger (`ledger_export.csv`)
- txn_id, post_date, description, amount, currency, category
Bank (`bank_export.csv`)
- bank_id, date, details, amount_usd
## Outputs
Written to `--outdir` (default example: `out/`)
- matched.csv
- exceptions.csv
- summary.json
- recon_report.xlsx
## How to run
1) Generate synthetic inputs:
   `python -m scripts.generate_data --outdir data/generated --n 60 --seed 42`

2) Run reconciliation:
   `python -m src.reconcile --ledger data/generated/ledger_export.csv --bank data/generated/bank_export.csv --outdir out`

3) Validate outputs:
   `python -m scripts.validate_outputs --outdir out`
## Matching rules (high level)
1) Deterministic exact match (highest confidence):
   - date + amount (cents) + normalized description

2) Conservative fallback match:
   - amount within 2 cents
   - date within 2 days
   - description similarity threshold (when both descriptions exist)
Unmatched or invalid rows become exceptions for human review.
## Troubleshooting
- “Missing required column …”
  - Confirm your input CSV headers match the expected columns above.

- “FAIL missing_file:…”
  - The reconcile step did not produce outputs. Re-run reconciliation and check for errors.

- Excel report not opening
  - Ensure `out/recon_report.xlsx` exists and open it manually from Finder if needed.

- Want a clean rerun
  - Delete outputs: `rm -f out/*` (or empty the folder in Finder)
