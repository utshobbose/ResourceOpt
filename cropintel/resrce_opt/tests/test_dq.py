# tests/test_dq.py
import pandas as pd
from cropintel.resrce_opt.dq.checks import coverage

def test_coverage_pass():
    df = pd.DataFrame({
        "district_code":["01","02","03","04"],
        "season":["aman"]*4,
        "year":[2025]*4
    })
    res = coverage(df, expected_districts=4, season="aman", year=2025)
    assert res.passed and res.details["pct"] == 100.0
