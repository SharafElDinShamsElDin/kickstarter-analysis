# Kickstarter Projects Analysis

A machine learning project that analyzes Kickstarter project data to predict project success using TensorFlow.

## Overview

This project processes Kickstarter project data, performs feature engineering, and builds a neural network model to predict whether a project will be successful or failed.

## Project Structure

- `import numpy as np.py` - Main analysis and model training script
- `ks-projects-201801.csv` - Kickstarter projects dataset

## Dependencies

- numpy
- pandas
- scikit-learn
- tensorflow

## Installation

```bash
pip install numpy pandas scikit-learn tensorflow
```

## Usage

Run the analysis script:

```bash
python "import numpy as np.py"
```

## Excel/xlwings integration

You can call the model directly from Excel using the [xlwings add-in](https://docs.xlwings.org/en/stable/installation.html).

1. Install xlwings and the add-in:
   ```bash
   pip install xlwings
   xlwings addin install
   ```
2. Configure the add-in to use your Python interpreter and point the **UDF Modules** setting to this repository folder so Excel can import `excel_integration.py`.
3. Train/export the model artifacts (see the modernized workflow below) and ensure the `artifacts/` folder is accessible from your workbook.
4. In Excel, place a campaign JSON payload in a cell (e.g., `A1`):
   ```json
   {
     "goal": 5000,
     "pledged": 1500,
     "backers": 42,
     "usd pledged": 1450,
     "category": "Technology",
     "main_category": "Technology",
     "currency": "USD",
     "country": "US",
     "deadline": "2024-12-01",
     "launched": "2024-10-01"
   }
   ```
5. Call the provided UDFs:
   - `=KICKSTARTER_SUCCESS_PROBABILITY(A1, "artifacts")` → decimal probability (0–1)
   - `=KICKSTARTER_SUCCESS_SUMMARY(A1, "artifacts")` → friendly verdict with percentage

The functions cache model artifacts per workbook session so repeated calls are fast. Update the `model_dir` argument if your artifacts live outside the default `artifacts/` folder.

## Modernized training and inference pipeline

The repository now includes a reusable training and inference module (`model_pipeline.py`) that is easier to call from Excel or any other client.

### Train and export artifacts

```
python model_pipeline.py train --csv /path/to/ks-projects-201801.csv --output-dir artifacts
```

The command trains the TensorFlow model, prints accuracy/AUC, and saves:

- `artifacts/kickstarter_model.keras` – trained network
- `artifacts/scaler.pkl` – feature scaler for inference
- `artifacts/feature_columns.json` – ordered feature list to align one-hot encoding

### Predict for a single campaign

Create a JSON file with the campaign data (e.g., `example_campaign.json`):

```json
{
  "goal": 5000,
  "pledged": 1500,
  "backers": 42,
  "usd pledged": 1450,
  "category": "Technology",
  "main_category": "Technology",
  "currency": "USD",
  "country": "US",
  "deadline": "2024-12-01",
  "launched": "2024-10-01"
}
```

Then run:

```
python model_pipeline.py predict --model-dir artifacts --json-path example_campaign.json
```

The script prints the predicted probability of success (0–1). A value above ~0.5 indicates a likely successful campaign.

### Example Bison prompt for the Excel plug-in

You can pair the TensorFlow model with your Bison-enabled Excel plug-in using a structured prompt:

```
System: You evaluate Kickstarter campaigns. Call the provided Python function predict_success_probability to score the campaign. Always echo the probability and a short rationale.

User: Will this campaign succeed?
Data (from Excel row): {serialized JSON for the row}
```

In the plug-in, map the Excel row to the JSON payload shown above, pass it to `predict_success_probability`, and return the numeric probability along with a short explanation based on the features (goal size, currency, timing, etc.).

## Features

- Data preprocessing and cleaning
- Feature engineering (temporal features extraction)
- One-hot encoding for categorical variables
- Data normalization using StandardScaler
- Train-test split for model evaluation

## Author

Your Name

## License

MIT
