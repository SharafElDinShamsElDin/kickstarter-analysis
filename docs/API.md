# Python API Reference

**Date:** June 2024

## Model Pipeline

### Load Model

```python
from src.model_pipeline import load_model

model, scaler, features = load_model()
```

Returns:
- `model` — TensorFlow/Keras model
- `scaler` — Feature scaler (StandardScaler)
- `features` — Feature names and mappings

### Make Predictions

```python
from src.model_pipeline import predict

probability = predict(
    campaign_data,  # dict with campaign info
    model,
    scaler,
    features
)
```

Returns: Float between 0 and 1 (probability of success)

## Excel Integration

### UDF Functions

```python
from src.excel_integration import (
    KICKSTARTER_SUCCESS_PROBABILITY,
    KICKSTARTER_SUCCESS_SUMMARY
)

# Direct call
prob = KICKSTARTER_SUCCESS_PROBABILITY(campaign_data)
summary = KICKSTARTER_SUCCESS_SUMMARY(campaign_data)
```

### Using in Excel

Register functions in `main.py`:

```python
import xlwings as xw

@xw.func
def my_predict(goal, pledged, backers):
    result = predict(...)
    return result
```

## Data Format

Campaign data dict:

```python
{
    'goal': 50000,
    'pledged': 75000,
    'backers': 150,
    'category': 'Technology',
    'country': 'US',
    'currency': 'USD',
    'deadline': '2024-12-31',
    'launched': '2024-01-01'
}
```

## Example Usage

```python
from src.model_pipeline import load_model, predict

# Load
model, scaler, features = load_model()

# Data
campaign = {
    'goal': 50000,
    'pledged': 75000,
    'backers': 200
}

# Predict
prob = predict(campaign, model, scaler, features)
print(f"Success probability: {prob:.2%}")
```
