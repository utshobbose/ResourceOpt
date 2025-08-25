# cropintel/resourceopt/io/files.py
import pandas as pd
from pathlib import Path

def read_csv(path: str|Path) -> pd.DataFrame:
    return pd.read_csv(path)

def write_json(text: str, path: str|Path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")
