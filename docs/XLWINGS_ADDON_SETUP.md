# Reinstall xlwings add-in for Excel

This file documents how to reinstall the xlwings add-in if functions are not showing up in the dropdown.

## Steps to Reinstall xlwings Add-in (macOS)

1. **Uninstall the current add-in:**
   ```bash
   source .venv/bin/activate
   xlwings uninstall
   ```

2. **Reinstall the add-in:**
   ```bash
   xlwings install
   ```

3. **Close Excel completely** (not just the window—quit the application).

4. **Reopen Excel and open a workbook** from the project folder (or the `excel_template.xlsx` in this repo).

5. **Check the xlwings Lite add-in:**
   - You should now see the project's custom functions in the dropdown:
     - `KICKSTARTER_SUCCESS_PROBABILITY`
     - `KICKSTARTER_SUCCESS_SUMMARY`

6. **Use the functions:**
   - Select the function from the dropdown.
   - Enter the required parameters (e.g., JSON campaign data in a cell).
   - Click the green "Run" button or press F5.

## If functions still don't appear

1. Verify `xlwings.conf` exists in the project root with correct module paths.
2. Verify `main.py` exists and imports the UDFs.
3. Check the xlwings version: `xlwings --version` (should be >= 0.30).
4. Restart Excel completely.
5. Check Excel's developer tools for any error messages (Tools > Macros > Edit Macros, then view the output/log).

## Alternative: Use RunPython from VBA

If the add-in still doesn't work, use the VBA macro approach:
- See `EXCEL_MACRO_INSTRUCTIONS.md` for steps to import `vba_module.bas` and create a `.xlsm` with a macro button.
