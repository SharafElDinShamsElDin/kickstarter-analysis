# xlwings Add-in Setup

**Date:** May 2024

## Installation

One-time setup:

```bash
xlwings install
```

## Enable Add-in

1. Open Excel
2. Go to Insert → Get Add-ins
3. Search for "xlwings"
4. Click Install

## Using UDF Functions

After install, in Excel:

1. Create a new workbook
2. Type formula: `=KICKSTARTER_SUCCESS_PROBABILITY(A1:K1)`
3. Press Enter

## Configuration

xlwings reads from `xlwings.conf` (in root folder):

```ini
[xlwings.telemetry]
enabled = True

[python]
version = 3.9
```

## Troubleshooting

**Functions don't appear:**
- Run: `xlwings uninstall`
- Run: `xlwings install`
- Restart Excel completely

**Module not found:**
- Check `src/` folder exists
- Check Python environment: `which python`
- Verify: `pip list | grep xlwings`

## Script Files

Located in `scripts/`:
- `excel_listener.py` — Auto-predict listener
- `create_branded_workbook.py` — Create workbook
- `setup_xlsm.py` — Setup macro support
