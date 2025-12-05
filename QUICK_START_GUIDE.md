# 🚀 Kickstarter Predictor - Quick Start Guide

## The Simplest Way to Use This Project

### **Option 1: Automatic Listener (RECOMMENDED & EASIEST) ⭐**

This is the simplest way to get predictions - **no macros, no button clicks needed!**

#### Step 1: Open Terminal
```bash
cd /Users/emkanlaptop/Desktop/model
source .venv/bin/activate
```

#### Step 2: Run the Listener
```bash
python scripts/excel_listener.py
```

**What happens:**
- Excel automatically opens with a template workbook
- The script monitors Excel for changes
- When you enter data and save, predictions appear instantly
- Continue entering campaigns and getting results

#### Step 3: Enter Campaign Data
In the Excel workbook that opens:
- **Row 5 onwards**: Enter your campaign data
- **Columns A-K**:
  - A: Goal (USD amount, e.g., 50000)
  - B: Pledged (USD amount, e.g., 75000)
  - C: Backers (number, e.g., 1250)
  - D: USD Pledged (same as B for USD projects)
  - E: Category (e.g., "Technology", "Design", "Film")
  - F: Main Category (auto-derived, can enter: "Technology", "Design", etc.)
  - G: Currency (e.g., "USD", "EUR", "GBP")
  - H: Country (e.g., "US", "UK", "DE")
  - I: Deadline (YYYY-MM-DD format, e.g., 2024-12-31)
  - J: Launched (YYYY-MM-DD format, e.g., 2024-09-01)

#### Step 4: Get Predictions
- **Column L**: Probability appears here after you save
  - 0.999981 = 99.99% chance of success
  - 0.75 = 75% chance
  - 0.02 = 2% chance

#### Step 5: Repeat
- Add more campaigns in rows 6, 7, 8, etc.
- Each will get predictions automatically

---

### **Option 2: Using the Branded Workbook (Also Easy)**

If you prefer not to have the listener running continuously:

#### Step 1: Open the Branded Workbook
```bash
open kickstarter_branded.xlsm
```

#### Step 2: (Optional) Install xlwings Add-in
If you want the toolbar buttons (one-time setup):
```bash
xlwings install
```

#### Step 3: Enter Data
- Edit the pre-formatted cells
- Save the workbook

#### Step 4: Get Predictions
**Option A - With Listener**
```bash
python scripts/excel_listener.py
```
Then enter data and save → predictions appear

**Option B - With Excel Formulas**
If you have xlwings installed, you can use:
```
=KICKSTARTER_SUCCESS_PROBABILITY(campaign_json, "artifacts")
```

---

### **Option 3: Quick Test with Sample Data**

Want to test without entering data?

```bash
python scripts/excel_listener.py
```

The template comes with example data in row 5. Just press Save and watch the prediction appear in column L!

---

## 📊 Example Walkthrough

### Campaign 1: Tech Product (High Success Rate)
```
Goal: 50,000
Pledged: 75,000
Backers: 1,250
Category: Technology
Country: US
Deadline: 2024-12-31

Result in Column L: 0.999981 = 99.99% Success ✅
```

### Campaign 2: Art Project (Medium Success Rate)
```
Goal: 10,000
Pledged: 7,500
Backers: 150
Category: Art
Country: US
Deadline: 2024-11-30

Result in Column L: 0.756 = 75.6% Success ⚠️
```

### Campaign 3: Underfunded Project (Low Success Rate)
```
Goal: 100,000
Pledged: 500
Backers: 5
Category: Film
Country: US
Deadline: 2024-10-31

Result in Column L: 0.0002 = 0.02% Success ❌
```

---

## ⚠️ Troubleshooting

### "Excel won't open when I run the listener"
```bash
# Make sure Excel is installed on your Mac
# Check if Excel is in Applications:
ls /Applications/Microsoft\ Excel.app

# If not found, install from Office or App Store
```

### "I get an error about model files not found"
```bash
# Make sure you're in the project directory
cd /Users/emkanlaptop/Desktop/model

# Check if model files exist
ls artifacts/
# Should show: kickstarter_model.keras, scaler.pkl, feature_columns.json
```

### "Predictions show 0 or don't update"
```bash
# 1. Make sure to SAVE the workbook after entering data
# 2. Wait 2-3 seconds for the listener to detect changes
# 3. Check the terminal for error messages
```

### "Which columns are required?"
All columns A-J should be filled:
- Goal, Pledged, Backers, USD Pledged
- Category, Main Category, Currency, Country
- Deadline, Launched

If any are missing, predictions may fail.

---

## 📁 File Structure Reminder

```
project/
├── kickstarter_branded.xlsm    ← The workbook to open
├── scripts/
│   └── excel_listener.py       ← The script that runs automatically
├── src/
│   ├── model_pipeline.py       ← The ML model
│   └── excel_integration.py    ← Prediction functions
└── artifacts/
    ├── kickstarter_model.keras ← Trained neural network
    ├── scaler.pkl              ← Feature scaler
    └── feature_columns.json    ← Feature names
```

---

## 🎯 Most Common Use Case

**For 90% of users, this is all you need:**

```bash
# Terminal 1: Navigate and activate environment
cd /Users/emkanlaptop/Desktop/model
source .venv/bin/activate

# Terminal 1: Run the listener
python scripts/excel_listener.py

# Then in Excel that opens:
# 1. Enter campaign data in row 5
# 2. Save the workbook (Cmd+S)
# 3. Prediction appears in column L
# 4. Repeat for more campaigns
```

That's it! ✨

---

## 📚 More Information

For detailed information, see:
- `README.md` - Project overview
- `BRANDED_WORKBOOK_GUIDE.md` - Workbook features
- `QUICKSTART_EXCEL_MACOS.md` - macOS-specific help
- `CUSTOMIZATION_SUMMARY.md` - Complete technical details

---

## 🎓 Model Info

- **Accuracy**: 92.08% (excellent!)
- **Trained on**: 37,887 real Kickstarter projects
- **Features**: 221 campaign attributes
- **Technology**: TensorFlow/Keras Neural Network

---

**Author**: Mohamed SharafEldin (202201849)  
**Email**: 12422021653750@pg.cu.edu.eg  
**Supervisors**: Dr. Tarek Ali, Prof. Mervat Gheith
