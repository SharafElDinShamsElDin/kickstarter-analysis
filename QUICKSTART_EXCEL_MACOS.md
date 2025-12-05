# Quick Start: Running the Kickstarter Model in Excel (macOS)

## Problem
The xlwings light plugin on macOS doesn't easily support programmatically-created form control buttons. Instead of fighting this limitation, we'll use a simple one-time setup approach.

## Solution: Two Options

### Option 1: Use the Listener (Automatic, No Macros) ✨ **Recommended**
1. Activate your virtualenv:
   ```bash
   source .venv/bin/activate
   ```
2. Run the listener:
   ```bash
   python excel_listener.py
   ```
3. Edit row 2 in the Excel sheet (`Predict` sheet) and save or change a value.
4. The Python script automatically detects the change, runs the model, and writes the probability into cell L2 (Result).
5. Press Ctrl+C in the terminal to stop the listener.

**Pros:** No macros, no VBA, no button to click—just edit and watch the model run.  
**Cons:** Requires a Python process running in the background.

---

### Option 2: Use Macros & a Button (On-Demand)
1. Create a macro-enabled workbook:
   ```bash
   source .venv/bin/activate
   python setup_xlsm.py
   ```
2. Follow the on-screen instructions:
   - Excel will open.
   - Go to **Tools > Macro > Edit Macros** (or Alt+F11).
   - File > **Import File...** > select `vba_module.bas`.
   - Close the VBA editor.
   - **File > Save As** > Format: **Excel Macro-Enabled Workbook (.xlsm)**.
   - Save as `kickstarter_predictor.xlsm`.
3. Close and reopen the `.xlsm` file. **Enable macros** when prompted.
4. Click the **Predict** button or go to **Tools > Macros > Run GetPrediction**.

**Pros:** On-demand—click a button to run the model. No background process.  
**Cons:** Requires macro import and macro security settings.

---

## Which Should I Choose?

| Scenario | Option 1 (Listener) | Option 2 (Macros) |
|----------|-------------------|-------------------|
| I want the simplest setup | ✓ | |
| I want real-time automatic predictions as I edit | ✓ | |
| I prefer clicking a button | | ✓ |
| I want no Python process running in background | | ✓ |

---

## Troubleshooting

### Listener doesn't detect changes
- Make sure you **save** the file after editing row 2, or edit a cell and press Enter.
- Check the terminal output—it should print "Detected input change" when it notices an update.

### Macros don't run / RunPython not found
- Ensure the xlwings add-in is installed: `pip install xlwings && xlwings install`.
- Check Excel > Preferences > Security & Privacy > Trust Center > Trusted Locations and allow the folder containing your `.xlsm`.
- Confirm macros are enabled in Excel before clicking the button.

### Model errors / Prediction fails
- Check the terminal output for error messages.
- Verify `artifacts/` contains the model files: `kickstarter_model.keras`, `scaler.pkl`, `feature_columns.json`.
- If using the macro, ensure the path in `vba_module.bas` points to your project folder (edit the `sys.path.append(...)` line if needed).

---

## Next Steps
Pick your approach and run the command above. Happy predicting! 🎉
