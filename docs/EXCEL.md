# Excel Integration

**Date:** April 2024

## Branded Workbook

File: `kickstarter_branded.xlsm`

**Features:**
- Blue-themed design with project branding
- Author attribution (Mohamed SharafEldin)
- Pre-formatted input/output sections
- Real-time prediction capability

## Using the Workbook

1. Open the Excel file:
   ```bash
   open kickstarter_branded.xlsm
   ```

2. Start the listener in another terminal:
   ```bash
   python scripts/excel_listener.py
   ```

3. Enter campaign data in row 2:
   - Column A: Campaign goal
   - Column B: Amount pledged
   - Column C: Number of backers
   - Additional columns: category, country, etc.

4. Save the file

5. Prediction appears in column L automatically

## Excel UDF Functions

Two custom functions available:

**KICKSTARTER_SUCCESS_PROBABILITY()**
- Returns probability (0-1)
- Usage: `=KICKSTARTER_SUCCESS_PROBABILITY(A2:K2)`

**KICKSTARTER_SUCCESS_SUMMARY()**
- Returns detailed analysis
- Usage: `=KICKSTARTER_SUCCESS_SUMMARY(A2:K2)`

## Creating Your Own Workbook

```bash
python scripts/create_branded_workbook.py
```

This generates a new workbook with all settings.
