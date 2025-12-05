"""
Author: Mohamed SharafEldin
Academic number: 202201849
Academic email: 12422021653750@pg.cu.edu.eg

Under Supervision of:
    - Dr. Tarek Ali, Faculty of Graduate Studies for Statistical Research
    - Prof. Mervat Gheith, Faculty of Graduate Studies for Statistical Research

Excel/xlwings bridge for the Kickstarter success model.

This module exposes light-weight user-defined functions (UDFs) that can be
registered with the xlwings add-in. The functions load the trained model
artifacts once, convert JSON from Excel into a Python dictionary, and return
probabilities that a campaign will succeed.

Usage example inside Excel (after configuring xlwings):

```
=KICKSTARTER_SUCCESS_PROBABILITY(A1)
=KICKSTARTER_SUCCESS_SUMMARY(A1, "artifacts")
```

Where cell ``A1`` contains a JSON string describing the campaign, e.g.:

```
{"goal": 5000, "pledged": 1500, "backers": 42, "usd pledged": 1450,
 "category": "Technology", "main_category": "Technology",
 "currency": "USD", "country": "US",
 "deadline": "2024-12-01", "launched": "2024-10-01"}
```
"""

import json
from pathlib import Path
from typing import Dict, Iterable, Tuple

import xlwings as xw

from model_pipeline import load_artifacts, predict_success_probability


_ARTIFACT_CACHE: Dict[str, Tuple[object, object, Iterable[str]]] = {}


def _load_cached_artifacts(model_dir: str) -> Tuple[object, object, Iterable[str]]:
    """Load model artifacts once per workbook session."""

    resolved_dir = str(Path(model_dir).expanduser().resolve())
    if resolved_dir not in _ARTIFACT_CACHE:
        model, scaler, feature_columns = load_artifacts(Path(resolved_dir))
        _ARTIFACT_CACHE[resolved_dir] = (model, scaler, feature_columns)
    return _ARTIFACT_CACHE[resolved_dir]


def _predict_from_json(campaign_json: str, model_dir: str) -> float:
    model, scaler, feature_columns = _load_cached_artifacts(model_dir)
    campaign_data = json.loads(campaign_json)
    return predict_success_probability(
        campaign_data, model=model, scaler=scaler, feature_columns=feature_columns
    )


@xw.func
@xw.arg(
    "campaign_json",
    doc=(
        "JSON describing the campaign (goal, pledged, backers, usd pledged, "
        "category, main_category, currency, country, deadline, launched)."
    ),
)
@xw.arg(
    "model_dir",
    doc=(
        "Directory containing kickstarter_model.keras, scaler.pkl, and "
        "feature_columns.json."
    ),
)
@xw.ret(expand="down")
def KICKSTARTER_SUCCESS_PROBABILITY(
    campaign_json: str, model_dir: str = "artifacts"
) -> float:
    """Return the predicted probability of success as a decimal between 0 and 1."""

    probability = _predict_from_json(campaign_json, model_dir)
    return round(probability, 6)


@xw.func
@xw.arg(
    "campaign_json",
    doc="Same JSON payload accepted by KICKSTARTER_SUCCESS_PROBABILITY.",
)
@xw.arg(
    "model_dir",
    doc=(
        "Directory containing kickstarter_model.keras, scaler.pkl, and "
        "feature_columns.json."
    ),
)
@xw.ret(expand="down")
def KICKSTARTER_SUCCESS_SUMMARY(
    campaign_json: str, model_dir: str = "artifacts"
) -> str:
    """Return a readable verdict with the probability percentage."""

    probability = _predict_from_json(campaign_json, model_dir)
    verdict = "Likely success" if probability >= 0.5 else "Needs improvement"
    return f"{verdict} — {probability:.2%} predicted success probability"
