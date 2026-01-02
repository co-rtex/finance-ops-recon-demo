
# Finance Ops Reconciliation Automation Demo (Synthetic Data Only)

A simple, auditable finance-ops reconciliation demo using only synthetic data.

## What it does
- Generates two synthetic CSV exports: a ledger export and a bank export
- Cleans/standardizes fields (dates, currency strings, whitespace/case)
- Matches transactions (exact match first, then a conservative fallback)
- Outputs audit-friendly files + an Excel report

## Quickstart (under 5 minutes)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 1) Generate synthetic inputs
python -m scripts.generate_data --outdir data/generated --n 60 --seed 42
# 2) Run reconciliation + Excel report
python -m src.reconcile \
  --ledger data/generated/ledger_export.csv \
  --bank data/generated/bank_export.csv \
  --outdir out
# 3) Validate outputs
python -m scripts.validate_outputs --outdir out
# 4) Open Excel report
open out/recon_report.xlsx
'
## Outputs
out/matched.csv

out/exceptions.csv

out/summary.json

out/recon_report.xlsx
