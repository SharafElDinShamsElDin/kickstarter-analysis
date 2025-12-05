"""
Create a simple UI button on the `Predict` sheet that calls the VBA macro `GetPrediction`.

Usage:
    python create_excel_ui.py

Notes:
- This script uses xlwings and the Excel COM API on Windows (and similar APIs on macOS). It attempts a few fallbacks to add a Form Control button.
- For the button to work, the workbook must contain the `GetPrediction` macro (import `vba_module.bas`) or the macro must be available in Personal Macro Workbook.
"""

import sys
from pathlib import Path

import xlwings as xw

TEMPLATE = Path("excel_template.xlsx")
SHEET = "Predict"


def add_button(sheet, left, top, width=100, height=30, caption="Predict"):
    """Try to add a Form Control button and assign OnAction to the GetPrediction macro."""
    try:
        # Try the Buttons().Add approach (commonly works on Windows)
        btn = sheet.api.Buttons().Add(left, top, width, height)
        try:
            btn.Caption = caption
        except Exception:
            try:
                btn.Text = caption
            except Exception:
                pass
        # Assign macro name (module-level macro in workbook)
        btn.OnAction = "GetPrediction"
        print("Button added via sheet.api.Buttons().Add")
        return True
    except Exception as e:
        print("Buttons().Add failed:", e)

    try:
        # Try Shapes.AddFormControl fallback (Type 1 is xlButtonControl on many systems)
        shp = sheet.api.Shapes.AddFormControl(1, left, top, width, height)
        try:
            shp.TextFrame.Characters().Text = caption
        except Exception:
            pass
        shp.OnAction = "GetPrediction"
        print("Button added via Shapes.AddFormControl")
        return True
    except Exception as e:
        print("Shapes.AddFormControl failed:", e)

    print("Failed to add a button programmatically. Please add a button manually and assign the macro 'GetPrediction'.")
    return False


def main():
    if not TEMPLATE.exists():
        print(f"Template not found: {TEMPLATE}. Run python excel_listener.py to create it, or create the Predict sheet manually.")
        sys.exit(1)

    app = xw.App(visible=True)
    try:
        wb = xw.Book(str(TEMPLATE))
    except Exception:
        wb = xw.books.open(str(TEMPLATE))

    sheet = wb.sheets[SHEET]

    # Determine a reasonable position next to the sample row
    rng = sheet.range("A2:J2")
    left = int(rng.left + rng.width + 10)
    top = int(rng.top)
    width = 90
    height = 30

    ok = add_button(sheet, left, top, width, height, caption="Predict")

    if ok:
        print("UI button created. Save the workbook as .xlsm to keep the button and macro association.")
    else:
        print("Could not create button programmatically. Add a button via Excel's Developer tab and assign 'GetPrediction'.")

    # Keep Excel open for user to test
    print("The workbook is open. Test the button after importing the VBA module and enabling macros.")


if __name__ == "__main__":
    main()
