import pandera as pa
from pandera import Column, DataFrameSchema, Check

AllocationSchema = DataFrameSchema(
    {
        "district_code": Column(pa.String, checks=Check.str_matches(r"^\d{2,4}$")),
        "season": Column(pa.String, checks=Check.isin(["aman","boro","aus"])),
        "year": Column(pa.Int, checks=Check.in_range(1990,2100)),
        "resource": Column(pa.String, checks=Check.isin(["urea","dap","mop","seed_aman","seed_boro"])),
        "requested_allocation_kg": Column(pa.Float, checks=Check.ge(0)),
        "feasible_demand_kg": Column(pa.Float, checks=Check.ge(0)),
    },
    coerce=True,
    strict=True
).add_checks([
    Check(lambda df: (df["requested_allocation_kg"] <= 1.2*df["feasible_demand_kg"]).all(),
        error="requested_allocation_kg exceeds 120% of feasible_demand_kg")
])