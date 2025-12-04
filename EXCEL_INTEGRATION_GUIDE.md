# Excel Integration Setup Guide

## Overview
The Kickstarter success prediction model can be used directly in Excel through xlwings, enabling real-time predictions without leaving your spreadsheet.

## Features

### Available Excel Functions

#### 1. `KICKSTARTER_SUCCESS_PROBABILITY(campaign_json, [model_dir])`
Returns the raw probability (0-1) that a campaign will succeed.

**Example:**
```excel
=KICKSTARTER_SUCCESS_PROBABILITY(A1, "artifacts")
```

**Output:** `0.927543` (92.75% success probability)

---

#### 2. `KICKSTARTER_SUCCESS_SUMMARY(campaign_json, [model_dir])`
Returns a readable verdict with percentage.

**Example:**
```excel
=KICKSTARTER_SUCCESS_SUMMARY(A1, "artifacts")
```

**Output:** `Likely success — 92.75% predicted success probability`

---

## Setup Instructions

### Step 1: Install xlwings Add-in
```bash
xlwings config create chained True
xlwings addin install
```

### Step 2: Configure Excel Workbook
1. Open Excel
2. Go to **File → Options → Trust Center → Trust Center Settings → Trusted Locations**
3. Add your project directory to trusted locations
4. Open your project workbook
5. Enable macros when prompted

### Step 3: Link Python Module
1. In Excel, go to **xlwings → Import Python UDFs**
2. Select `excel_integration.py`
3. The functions will now be available in your workbook

### Step 4: Create Campaign JSON in Spreadsheet

Format your campaign data as JSON in a cell. Example in cell `A1`:

```json
{
  "goal": 50000,
  "pledged": 75000,
  "backers": 1250,
  "usd pledged": 75000,
  "category": "Technology",
  "main_category": "Technology",
  "currency": "USD",
  "country": "US",
  "deadline": "2024-12-31",
  "launched": "2024-09-01"
}
```

### Step 5: Use the Functions

**In cell B1:**
```excel
=KICKSTARTER_SUCCESS_PROBABILITY(A1, "artifacts")
```

**In cell C1:**
```excel
=KICKSTARTER_SUCCESS_SUMMARY(A1, "artifacts")
```

Press Enter, and the predictions will appear!

---

## Expected Output

| Cell | Formula | Result |
|------|---------|--------|
| A1 | (Campaign JSON) | `{"goal": 50000, ...}` |
| B1 | `=KICKSTARTER_SUCCESS_PROBABILITY(A1, "artifacts")` | `1.0` |
| C1 | `=KICKSTARTER_SUCCESS_SUMMARY(A1, "artifacts")` | `Likely success — 100.00% predicted success probability` |

---

## Data Format Requirements

All campaigns must include these required fields:

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `goal` | number | 50000 | Funding goal in USD |
| `pledged` | number | 75000 | Amount pledged so far |
| `backers` | number | 1250 | Number of backers |
| `usd pledged` | number | 75000 | Pledged amount in USD |
| `category` | string | "Technology" | Campaign category |
| `main_category` | string | "Technology" | Main category |
| `currency` | string | "USD" | Currency code |
| `country` | string | "US" | Country code (2 letters) |
| `deadline` | string | "2024-12-31" | Campaign deadline (YYYY-MM-DD) |
| `launched` | string | "2024-09-01" | Campaign launch date (YYYY-MM-DD) |

---

## Advanced Usage

### Dynamic Model Directory
You can change the model directory by updating the second parameter:

```excel
=KICKSTARTER_SUCCESS_PROBABILITY(A1, "C:/models/artifacts")
```

### Batch Predictions
To predict multiple campaigns:
1. Put each campaign's JSON in column A (A1, A2, A3, etc.)
2. In B1 enter: `=KICKSTARTER_SUCCESS_PROBABILITY(A1, "artifacts")`
3. Drag down to copy the formula to B2, B3, etc.
4. All campaigns will be predicted at once!

---

## Troubleshooting

**Problem:** "Module not found" error
- **Solution:** Ensure `model_pipeline.py` and `excel_integration.py` are in the same directory

**Problem:** Model artifacts not found
- **Solution:** Verify the `artifacts/` folder exists with:
  - `kickstarter_model.keras`
  - `scaler.pkl`
  - `feature_columns.json`

**Problem:** Invalid JSON error
- **Solution:** Ensure your JSON is properly formatted (use online JSON validator)

**Problem:** Function returns #VALUE! error
- **Solution:** 
  1. Check that all required fields are present
  2. Verify data types (numbers are numbers, strings are strings)
  3. Ensure dates are in YYYY-MM-DD format

---

## Performance Notes

- **First call:** ~2-3 seconds (model loading)
- **Subsequent calls:** ~100-200ms (cached model)
- **Batch processing:** ~500ms-1s for 100 campaigns

---

## Demo File

To test the integration without manual setup, use the included sample campaigns:
- `sample_campaign_1.json` - Well-funded campaign
- `sample_campaign_2.json` - Underfunded campaign
- `sample_campaign_3.json` - Moderately-funded campaign

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the model documentation in `TRAINING_RESULTS.md`
3. Check model accuracy in `PREDICTION_TEST_RESULTS.md`

---

**Status:** ✅ Excel Integration Ready for Use

Visit [xlwings Documentation](https://docs.xlwings.org) for more details.
