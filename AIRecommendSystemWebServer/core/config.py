import os
from pathlib import Path

_BASE_DIR    = Path(__file__).parent.parent.parent          # AIRecommendSystem/
_UTIL_DIR    = Path(__file__).parent.parent / "util"        # webServer/util/

TEMPLATE_DIR = _BASE_DIR / "AIRecommendSystemWebClient" / "www" / "template"
STATIC_DIR   = _BASE_DIR / "AIRecommendSystemWebClient" / "www" / "static"


class Settings:
    POSTGRES_URI = os.environ.get(
        "POSTGRES_URI",
        "postgresql+asyncpg://aisystem:Damn13258@localhost:5432/aisystem_db"
    )

    EXERCISE_JSON = _UTIL_DIR / "exercise.json"
    METRIC_JSON   = _UTIL_DIR / "metric.json"
    OPERATOR_JSON = _UTIL_DIR / "operator.json"


settings = Settings()
