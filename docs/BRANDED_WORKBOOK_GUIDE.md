# Branded Excel Workbook Guide

## Overview

The **Kickstarter Success Predictor** project includes a custom-branded Excel workbook (`kickstarter_branded.xlsm`) with professional styling and blue color scheme reflecting the project branding.

## Features

### 🎨 Visual Branding
- **Color Scheme**: Professional blue (#2E75B6 primary, #4472C4 accent)
- **Logo**: Blue header with project title "🚀 Kickstarter Success Predictor"
- **Author Attribution**: Prominent display of Mohamed SharafEldin and supervisors
- **Professional Layout**: Clean input/output sections with clear structure

### 📊 Workbook Structure

#### Row 1: Title Section
- Full-width blue header with project name
- White text, 16pt bold font
- Height: 30px for visibility

#### Row 2: Author Information
- Accent blue background (#4472C4)
- Displays: Author name (202201849), Supervisors (Dr. Tarek Ali, Prof. Mervat Gheith)
- Italic 10pt font for secondary importance

#### Row 4: Column Headers (Blue)
Campaign input fields:
- Goal
- Pledged
- Backers
- USD Pledged
- Category
- Main Category
- Currency
- Country
- Deadline
- Launched
- **Probability** (output column)

#### Row 5: Example Data
Pre-filled with sample campaign:
- Goal: $50,000
- Pledged: $75,000
- Backers: 1,250
- Category: Technology
- Result: Ready for prediction

### 🔧 How to Use

#### Option 1: With xlwings Add-in (Recommended for macOS)
```bash
# 1. Create the branded workbook (already done)
python scripts/create_branded_workbook.py

# 2. Install xlwings add-in
xlwings addin install

# 3. Open the workbook
open kickstarter_branded.xlsm

# 4. Start excel_listener.py to auto-predict
python scripts/excel_listener.py
```

#### Option 2: With Macro Buttons (Windows/Excel 2013+)
Follow instructions in `EXCEL_MACRO_INSTRUCTIONS.md`

### 📝 Entering Campaign Data

1. **Row 5 Template**:
   - Columns A-J: Campaign parameters
   - Column L: Prediction probability (auto-populated)

2. **Adding Multiple Campaigns**:
   - Copy row 5 formatting to new rows
   - Fill in campaign data
   - Run predictions (automatic with listener or via button)

3. **Supported Categories**:
   - Technology, Design, Film, Music, Art, Publishing, Food, Comics, Theater, Games, Fashion, Photography, Crafts, Journalism, Dance

### 🎯 Example Predictions

The workbook includes sample data for testing:

**Sample Campaign 1** (Technology - High Success):
- Goal: $50,000 → Pledged: $75,000
- Prediction: 100.00% (likely to succeed)

**Sample Campaign 2** (Underfunded Project):
- Goal: $100,000 → Pledged: $200
- Prediction: 0.02% (very unlikely)

**Sample Campaign 3** (Medium Risk):
- Goal: $30,000 → Pledged: $22,794
- Prediction: 75.93% (good chance)

### 🛠️ Customization

#### Change Project Name
Edit in `scripts/create_branded_workbook.py` (line ~79):
```python
title_cell.value = "Your Project Name Here"
```

#### Change Author Info
Update author cell (line ~87):
```python
author_cell.value = "Your Name (Your ID) | Your Supervisors"
```

#### Adjust Colors
Modify hex codes in script:
- Primary blue: `2E75B6` (line ~77)
- Accent blue: `4472C4` (line ~85)
- Light background: `E7F0F7` (line ~107)

### 🔗 Integration Points

**Model Layer**:
- Model: `artifacts/kickstarter_model.keras`
- Scaler: `artifacts/scaler.pkl`
- Features: `artifacts/feature_columns.json`

**Excel Layer**:
- UDFs: `src/excel_integration.py`
  - `KICKSTARTER_SUCCESS_PROBABILITY(campaign_json, model_dir)`
  - `KICKSTARTER_SUCCESS_SUMMARY(campaign_json, model_dir)`
- Listener: `scripts/excel_listener.py` (auto-predict mode)

**Configuration**:
- xlwings config: `xlwings.conf` (root and `excel/`)
- Custom ribbon: `excel/customRibbon.xml` (optional)

### 📊 Data Format

When entering campaign data:
- **Goal & Pledged**: Numeric values (USD)
- **Backers**: Integer count
- **Category**: Select from list (case-sensitive)
- **Main Category**: Auto-derived from category
- **Currency**: ISO 4217 code (USD, EUR, GBP, etc.)
- **Country**: Country code (US, UK, DE, etc.)
- **Dates**: YYYY-MM-DD format

### ⚠️ Troubleshooting

#### "Ribbon not showing"
- This is normal on some platforms
- Workbook still fully functional
- Use `excel_listener.py` for automatic predictions

#### "Macro security warning"
- Click "Enable Content" when prompted
- Required for xlwings integration

#### "Column not visible"
- Scroll right to see the Probability column (L)
- Or use `View → Freeze Panes` to lock columns

#### "Data entry errors"
- Ensure all campaigns have same column structure
- Check category spelling matches model training data

### 🚀 Next Steps

1. **Test Locally**: Open workbook, enter data, verify predictions
2. **Share Template**: Distribute branded workbook to stakeholders
3. **Automate Batch**: Use `excel_listener.py` for hands-off predictions
4. **Customize Further**: Adjust colors, headers, fields per your needs

### 📚 Related Documentation

- `QUICKSTART_EXCEL_MACOS.md` — Quick setup for macOS
- `EXCEL_INTEGRATION_GUIDE.md` — Detailed Excel integration
- `EXCEL_MACRO_INSTRUCTIONS.md` — VBA macro setup
- `XLWINGS_ADDON_SETUP.md` — xlwings add-in troubleshooting

### 📧 Contact

**Author**: Mohamed SharafEldin (202201849)
**Email**: 12422021653750@pg.cu.edu.eg
**Supervisors**: Dr. Tarek Ali, Prof. Mervat Gheith
**Faculty**: Faculty of Graduate Studies for Statistical Research

---

**Generated**: 2024
**Project**: Kickstarter Success Prediction Model
**Model Accuracy**: 92.08% (Validation), AUC: 0.9780
