from .checks import DQResult
import json
from datetime import datetime

def to_json(results: list[DQResult]) -> str:
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "summary": {"passed": all(r.passed for r in results),
                    "total": len(results),
                    "failed": [r.name for r in results if not r.passed]},
        "results": [r.__dict__ for r in results],
        "version": 1
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)