# cropintel/resourceopt/cli.py
import typer, yaml, pandas as pd
from .schemas.signals_schema import SignalsSchema
from .schemas.allocation_schema import AllocationSchema
from .dq import checks, reconcile, report
from .io.files import read_csv, write_json

app = typer.Typer(add_completion=False)

@app.command()
def validate(signals_csv: str, alloc_csv: str, national_caps_csv: str,
             expected_districts: int, season: str, year: int, out: str="dq_report.json"):
    cfg = yaml.safe_load(open("cropintel/resourceopt/config/data_contract.yaml","r"))
    signals = SignalsSchema.validate(read_csv(signals_csv))
    alloc = AllocationSchema.validate(read_csv(alloc_csv))
    caps = pd.read_csv(national_caps_csv)

    results = []
    results.append(checks.coverage(signals, expected_districts, season, year))
    results.append(checks.reconciliation(alloc, caps))
    results += checks.ranges(signals, {
        "disease_risk_index": (0,1),
        "soil_fertility_index": (0,1),
        "yield_responsiveness_index": (0,1),
        "irrigation_coverage_pct": (0,100),
    })

    write_json(report.to_json(results), out)
    typer.echo(f"Wrote {out}. PASS={all(r.passed for r in results)}")

if __name__ == "__main__":
    app()
