# Finance Ops Reconciliation Automation Demo (Synthetic Data Only)

A simple, auditable reconciliation demo for finance operations workflows using **only synthetic data**.

## Quickstart (under 5 minutes)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1) Generate synthetic CSV exports
python -m scripts.generate_data --outdir data/generated --n 60 --seed 42

# 2) Run reconciliation + Excel report
python -m src.reconcile \
  --ledger data/generated/ledger_export.csv \
  --bank data/generated/bank_export.csv \
  --outdir out

# 3) Validate outputs (light QA)
python -m scripts.validate_outputs --outdir out

