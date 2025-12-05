"""
xlwings Lite configuration and UDF entry point.

This file is scanned by the xlwings Lite add-in. Any functions decorated with @xw.func 
are automatically exposed in the add-in's dropdown menu in Excel.

To use:
1. Ensure this file is named 'main.py' or is referenced in xlwings.conf.
2. The xlwings add-in will scan for @xw.func decorators and expose them as custom functions.
3. In Excel, use the xlwings Lite dropdown to select and run functions.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path so imports work when called from Excel
sys.path.insert(0, str(Path(__file__).parent))

from excel_integration import KICKSTARTER_SUCCESS_PROBABILITY, KICKSTARTER_SUCCESS_SUMMARY

# Re-export the UDFs so xlwings can discover them
__all__ = ['KICKSTARTER_SUCCESS_PROBABILITY', 'KICKSTARTER_SUCCESS_SUMMARY']
