# Quick Start Guide

**Date:** January 2024

## Installation

```bash
git clone https://github.com/SharafElDinShamsElDin/kickstarter-analysis.git
cd kickstarter-analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Verify Setup

```bash
python test_full_project.py
```

All 6 tests should pass ✅

## Usage

### Option 1: Excel (Recommended)
```bash
open kickstarter_branded.xlsm
python scripts/excel_listener.py
```

### Option 2: Python
```python
from src.model_pipeline import load_model, predict
model, scaler, features = load_model()
result = predict(campaign_data, model, scaler, features)
```

## File Structure

- `src/` — Python code
- `scripts/` — Helper scripts
- `data/` — Training data
- `artifacts/` — Model files
- `tests/` — Test suite
- `excel/` — Excel files
