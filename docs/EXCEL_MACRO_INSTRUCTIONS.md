# Creating a macro-enabled Excel workbook (.xlsm) for the Kickstarter predictor

This repository provides two safe options to run predictions from Excel:

- Run-time bridge (no macros): `excel_listener.py` opens a workbook, polls the sample row, runs the model and writes the result.
- On-demand button (recommended): create a macro-enabled workbook (`.xlsm`) that calls `RunPython` from xlwings and invokes `vba_predict` in `excel_integration.py`.

This document helps you create a ready-to-use `.xlsm` locally (one-time steps) and includes a small helper to open the template.

---

Requirements
- Python environment with the project's dependencies (see `requirements.txt`): `xlwings`, `openpyxl` (for template creation) and your virtualenv activated when Excel calls Python.
- Excel installed on your machine (macOS or Windows). Enable macros when prompted.
- xlwings add-in installed and configured (see https://docs.xlwings.org).

Files added to the repo
- `vba_module.bas` — a plain text VBA module you can import into Excel's VBA editor. It contains the `GetPrediction` macro that calls xlwings' `RunPython`.
- `open_excel_template.sh` — a macOS helper script that opens the template workbook (`excel_template.xlsx`) using the default app (Excel).

Steps to create a ready `.xlsm`
1. Open a terminal and activate your project's virtual environment, e.g.:

```bash
source .venv/bin/activate
pip install -r requirements.txt openpyxl
```

2. If you don't already have `excel_template.xlsx`, generate it by running (this repository includes `excel_listener.py` which will create one automatically if missing). Alternatively, create a workbook with one sheet named `Predict` and place headers in row 1:

```
A1: goal
B1: pledged
C1: backers
D1: usd pledged
E1: category
F1: main_category
G1: currency
H1: country
I1: deadline
J1: launched
L1: Result
```

3. Save the workbook as `kickstarter_predictor.xlsm` (macro-enabled workbook).

4. Open Excel and press `Alt+F11` (Windows) or use the Developer menu to open the VBA editor on macOS.

5. In the VBA editor, Import the file `vba_module.bas` (File → Import File...) which adds the `GetPrediction` macro to the workbook.

6. Edit the `GetPrediction` VBA code if necessary to point to your project path. The default uses `/Users/emkanlaptop/Desktop/model`; change this to the absolute path of your project folder.

7. Optionally add a button to the `Predict` sheet and assign `GetPrediction` to it.

8. Make sure the Python interpreter that xlwings uses is the one from your virtualenv. On macOS, xlwings will use the interpreter set in the xlwings add-in preferences or you can set an explicit sys.path inside the macro as done in `vba_module.bas`.

9. Click the button in Excel. The macro will run `RunPython` which imports `excel_integration.vba_predict` and writes the prediction in `L2`.

Troubleshooting
- If Excel reports that RunPython cannot be found, confirm the xlwings add-in is installed and enabled. See: https://docs.xlwings.org/en/stable/addin.html
- If Python cannot import the project modules, edit the `sys.path.append(...)` in the VBA macro to point to the absolute path for this repo.
- MacOS: Excel's security settings may block macros; enable macros and trust the location of the file.

Security note
- The `.xlsm` file contains a macro; treat it like any macro-enabled file and only enable macros for files you trust.

If you'd like, I can also produce a small shell script that automates the `xlsm` creation by opening Excel then pausing for you to import the `vba_module.bas` and save as .xlsm — let me know if you want that.
