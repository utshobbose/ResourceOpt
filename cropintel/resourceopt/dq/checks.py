from dataclasses import dataclass
import pandas as pd

@dataclass
class DQResult:
    name: str
    passed: bool
    details: dict

def coverage(signals: pd.DataFrame, expected_districts: int, season: str, year: int) -> DQResult:
    subset = signals.query("season == @season and year == @year")["district_code"].nunique()
    pct = 100 * subset / expected_districts if expected_districts else 0
    return DQResult(
        name="coverage",
        passed=pct >= 98,
        details={"found": subset, "expected": expected_districts, "pct": round(pct,2)}
    )

def reconciliation(district_alloc: pd.DataFrame, national_caps: pd.DataFrame) -> DQResult:
    # national_caps: columns [season, year, resource, national_cap_kg]
    merged = (district_alloc
            .groupby(["season","year","resource"], as_index=False)["requested_allocation_kg"].sum()
            .merge(national_caps, on=["season","year","resource"], how="left"))
    merged["abs_pct_diff"] = (merged["requested_allocation_kg"] - merged["national_cap_kg"]).abs() / merged["national_cap_kg"]
    offending = merged[merged["abs_pct_diff"] > 0.01]
    return DQResult(
        name="reconciliation",
        passed=offending.empty,
        details={"offending": offending.to_dict(orient="records")}
    )

def ranges(df: pd.DataFrame, spec: dict) -> list[DQResult]:
    results = []
    for col, (lo, hi) in spec.items():
        bad = df[(df[col] < lo) | (df[col] > hi)]
        results.append(DQResult(
            name=f"range::{col}",
            passed=bad.empty,
            details={"violations": len(bad)}
        ))
    return results