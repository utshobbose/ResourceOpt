import pandas as pd

def compute_feasible_demand(cultivated: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
    # cultivated: [district_code, season, year, cultivated_area_ha, crop]
    # rates: [crop, resource, kg_per_ha]
    return (cultivated
    .merge(rates, on="crop")
    .assign(feasible_demand_kg=lambda d: d["cultivated_area_ha"]*d["kg_per_ha"])
    [["district_code","season","year","resource","feasible_demand_kg"]])

def greedy_feasibility_check(demand_df: pd.DataFrame, national_available_kg: float) -> bool:
    # simple feasibility: sum of min(demand, remaining) should allocate without breaking caps
    remaining = national_available_kg
    for _, row in demand_df.sort_values("feasible_demand_kg", ascending=False).iterrows():
        take = min(row.feasible_demand_kg, remaining)
        remaining -= take
        if remaining < 0:  # shouldn’t happen
            return False
    return national_available_kg <= demand_df.feasible_demand_kg.sum()