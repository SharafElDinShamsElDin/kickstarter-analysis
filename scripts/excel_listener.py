"""
Excel listener: opens an Excel template and waits for the user to enter a sample campaign in the "Sample Input" row.
When the row changes, it calls the project's prediction function and writes the probability into the sheet.

Usage:
  1. Activate your project's virtualenv where `xlwings` is installed.
  2. Run: python excel_listener.py
  3. Excel will open the template (created automatically if missing). Edit the row under the headers and save.
  4. The script will detect the change, run the model, and write the probability in the Result column.

Notes:
- Requires xlwings and openpyxl installed in the Python environment used to run this script.
- Model artifacts are expected in `./artifacts` (kickstarter_model.keras, scaler.pkl, feature_columns.json).
"""

import time
import json
import os
import sys
from pathlib import Path

# Add src/ to path so we can import from the project
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    import xlwings as xw
except Exception as e:
    raise SystemExit("xlwings is required. Install with: pip install xlwings")

TEMPLATE = "excel_template.xlsx"
SHEET = "Predict"
HEADER_RANGE = "A1:J1"
INPUT_RANGE = "A2:J2"
RESULT_CELL = "L2"

EXAMPLE_HEADERS = [
    "goal",
    "pledged",
    "backers",
    "usd pledged",
    "category",
    "main_category",
    "currency",
    "country",
    "deadline",
    "launched",
]

EXAMPLE_ROW = [
    50000,
    75000,
    1250,
    75000,
    "Technology",
    "Technology",
    "USD",
    "US",
    "2024-12-31",
    "2024-09-01",
]


def create_template(path: str):
    """Create a simple template Excel workbook if it doesn't exist."""
    try:
        from openpyxl import Workbook
    except Exception:
        raise SystemExit("openpyxl is required to generate the template. Install with: pip install openpyxl")

    wb = Workbook()
    ws = wb.active
    ws.title = SHEET

    # Write headers and example row
    ws.append(EXAMPLE_HEADERS)
    ws.append(EXAMPLE_ROW)

    # Add a Result header and leave cell blank for output
    ws.cell(row=1, column=12, value="Result")
    wb.save(path)
    print(f"Created template: {path}")


def read_input_row(sheet):
    vals = sheet.range(INPUT_RANGE).value
    # If user enters a single value in first cell, xlwings may return scalar; normalize to list
    if vals is None:
        return None
    if not isinstance(vals, list):
        # single cell selected
        vals = [vals]
    return vals


def build_campaign_from_row(headers, values):
    # Trim values list to headers length
    values = values[: len(headers)]
    campaign = {h: v for h, v in zip(headers, values)}
    # Try to convert numeric fields back to proper types where reasonable
    for key in ["goal", "pledged", "backers", "usd pledged"]:
        if key in campaign and campaign[key] is not None:
            try:
                campaign[key] = int(campaign[key])
            except Exception:
                try:
                    campaign[key] = float(campaign[key])
                except Exception:
                    pass
    return campaign


def main():
    # Generate template if missing
    path = Path(TEMPLATE)
    if not path.exists():
        create_template(TEMPLATE)

    print("Opening Excel and waiting for input. Edit the sample row (row 2) and save or change a value to trigger prediction.")
    app = xw.App(visible=True)

    try:
        wb = xw.Book(str(path))
    except Exception:
        # If already open, connect
        wb = xw.books.open(str(path))

    sheet = wb.sheets[SHEET]

    headers = sheet.range(HEADER_RANGE).value
    if not headers or not isinstance(headers, list):
        headers = EXAMPLE_HEADERS

    # Read initial state
    last_values = read_input_row(sheet)

    try:
        # Lazy import of the project's prediction helper
        from excel_integration import KICKSTARTER_SUCCESS_PROBABILITY
    except Exception as e:
        print("Warning: could not import excel_integration.KICKSTARTER_SUCCESS_PROBABILITY. Make sure your PYTHONPATH is set and artifacts exist.")
        print(str(e))
        return

    print("Template open. Waiting for changes to the sample input row...")

    try:
        while True:
            time.sleep(1)
            current_values = read_input_row(sheet)
            if current_values is None:
                continue
            # If changed from last time and not just the example
            if current_values != last_values:
                last_values = current_values
                campaign = build_campaign_from_row(headers, current_values)
                campaign_json = json.dumps(campaign)
                print("Detected input change. Running prediction for:")
                print(campaign)

                try:
                    prob = KICKSTARTER_SUCCESS_PROBABILITY(campaign_json, model_dir="./artifacts")
                    # Write probability into the result cell
                    sheet.range(RESULT_CELL).value = prob
                    print(f"Probability: {prob:.6f} ({prob*100:.2f}%) written to {RESULT_CELL}")
                except Exception as e:
                    print("Prediction failed:", e)

    except KeyboardInterrupt:
        print("Listener stopped by user.")
    finally:
        # Keep the workbook open but close the app if desired
        try:
            app.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
