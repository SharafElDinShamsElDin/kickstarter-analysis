#!/usr/bin/env bash
# macOS helper: open the excel template in default app (Excel)
# Usage: ./open_excel_template.sh
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$PROJECT_ROOT/excel_template.xlsx"

if [ ! -f "$TEMPLATE" ]; then
  echo "Template not found: $TEMPLATE"
  echo "You can generate it by running python ../scripts/excel_listener.py or create a workbook named Predict with the required headers."
  exit 1
fi

open "$TEMPLATE"
