# Finance Ops Reconciliation Automation Demo (Synthetic Data Only)

Quickstart:
1) Create synthetic data
2) Run reconciliation
3) View outputs in /out

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m scripts.generate_data --outdir data/generated
python -m src.reconcile --ledger data/generated/ledger_export.csv --bank data/generated/bank_export.csv --outdir out
ls -lah out

