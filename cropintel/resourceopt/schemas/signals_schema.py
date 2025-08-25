import pandera as pa
from pandera import Column, DataFrameSchema, Check

SignalsSchema = DataFrameSchema(
    {
        "district_code": Column(pa.String, checks=Check.str_matches(r"^\d{2,4}$")),
        "season": Column(pa.String, checks=Check.isin(["aman","boro","aus"])),
        "year": Column(pa.Int, checks=Check.in_range(1990, 2100)),
        "disease_risk_index": Column(pa.Float, checks=Check.in_range(0,1)),
        "rainfall_mm": Column(pa.Float, checks=Check.ge(0)),
        "rainfall_anomaly_pos": Column(pa.Float, checks=Check.in_range(0,1)),
        "prior_deficit_kg": Column(pa.Float, checks=Check.ge(0)),
        "soil_fertility_index": Column(pa.Float, checks=Check.in_range(0,1)),
        "yield_responsiveness_index": Column(pa.Float, checks=Check.in_range(0,1)),
        "cultivated_area_ha": Column(pa.Float, checks=Check.ge(0)),
        "irrigation_coverage_pct": Column(pa.Float, checks=Check.in_range(0,100)),
    },
    coerce=True,
    strict=True
)