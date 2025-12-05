# Kickstarter Success Prediction Model

A machine learning model that predicts the probability of Kickstarter campaign success using TensorFlow/Keras, integrated with Excel via xlwings.

## Project Structure

```
.
├── src/                            # Python source modules
│   ├── model_pipeline.py          # ML pipeline (train, predict, load artifacts)
│   ├── excel_integration.py       # xlwings UDF functions for Excel
│   ├── main.py                    # xlwings entry point (UDF discovery)
│   └── train_notebook_export.py   # Training script (exported from notebook)
│
├── scripts/                        # Helper scripts and CLI tools
│   ├── excel_listener.py          # Listener: opens Excel, polls for sample input
│   ├── setup_xlsm.py              # Helper: creates .xlsm with macro
│   ├── create_excel_ui.py         # Helper: adds Predict button to workbook
│   └── open_excel_template.sh     # macOS helper: opens template in Excel
│
├── docs/                          # Documentation
│   ├── README.md                  # Quick start guide
│   ├── AUTHORS.md                 # Author and supervisor info
│   ├── TRAINING_RESULTS.md        # Training metrics and results
│   ├── PREDICTION_TEST_RESULTS.md # Sample prediction outputs
│   ├── PROJECT_RESULTS.md         # Comprehensive project summary
│   ├── QUICKSTART_EXCEL_MACOS.md  # macOS Excel quick start
│   ├── XLWINGS_ADDON_SETUP.md     # xlwings add-in setup guide
│   ├── EXCEL_INTEGRATION_GUIDE.md # Excel integration details
│   └── EXCEL_MACRO_INSTRUCTIONS.md# VBA macro setup
│
├── data/                          # Data files
│   ├── ks-projects-201801.csv     # Kickstarter projects dataset
│   └── sample_campaign_*.json     # Sample campaigns for testing
│
├── tests/                         # Test suite
│   └── test_excel_integration.py  # Excel integration tests
│
├── excel/                         # Excel-specific files
│   ├── vba_module.bas             # VBA macro code for .xlsm
│   └── xlwings.conf               # (also in root for discovery)
│
├── artifacts/                     # Trained model artifacts
│   ├── kickstarter_model.keras    # Trained TensorFlow model
│   ├── scaler.pkl                 # Feature scaling transformer
│   └── feature_columns.json       # Feature column names
│
├── xlwings.conf                   # xlwings configuration (root)
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
└── README.md                      # (this file)
```

## Quick Start

### Prerequisites
- Python 3.7+ with venv
- Excel (macOS or Windows)
- xlwings installed

### Installation

1. **Clone and set up environment:**
   ```bash
   git clone https://github.com/SharafElDinShamsElDin/kickstarter-analysis.git
   cd kickstarter-analysis
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or: .venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up xlwings add-in (one-time):**
   ```bash
   xlwings install
   ```

### Usage

#### Option 1: Automatic (Listener) — **Recommended for simplicity**
```bash
cd scripts
python excel_listener.py
```
- Excel opens with a template.
- Edit row 2 (sample input) and save.
- The script automatically detects changes and writes predictions to cell L2.

**See:** `docs/QUICKSTART_EXCEL_MACOS.md` for full details.

#### Option 2: xlwings Add-in (Dropdown Functions)
1. Open Excel and a workbook from this folder.
2. Look for the **xlwings Lite** add-in in the ribbon.
3. Select custom functions from the dropdown:
   - `KICKSTARTER_SUCCESS_PROBABILITY`
   - `KICKSTARTER_SUCCESS_SUMMARY`
4. Click **Run** or press F5.

**See:** `docs/XLWINGS_ADDON_SETUP.md` for troubleshooting.

#### Option 3: VBA Macros (Button Click)
1. Create a macro-enabled workbook (.xlsm):
   ```bash
   cd scripts
   python setup_xlsm.py
   ```
2. Follow on-screen instructions to import `excel/vba_module.bas`.
3. Save as `.xlsm` and enable macros when opening.
4. Click the Predict button.

**See:** `docs/EXCEL_MACRO_INSTRUCTIONS.md` for detailed steps.

## Model Details

- **Framework:** TensorFlow/Keras (Sequential neural network)
- **Input:** Kickstarter campaign features (goal, pledged, backers, category, country, dates, etc.)
- **Output:** Probability of campaign success (0–1)
- **Validation Accuracy:** 92.08% (AUC: 0.9780)

**See:** `docs/TRAINING_RESULTS.md` for metrics and `docs/PROJECT_RESULTS.md` for full summary.

## Project Information

**Author:** Mohamed SharafEldin  
**Academic Number:** 202201849  
**Email:** 12422021653750@pg.cu.edu.eg

**Supervisors:**
- Dr. Tarek Ali, Faculty of Graduate Studies for Statistical Research
- Prof. Mervat Gheith, Faculty of Graduate Studies for Statistical Research

**Repository:** https://github.com/SharafElDinShamsElDin/kickstarter-analysis

## Documentation

- `docs/README.md` — Main documentation
- `docs/QUICKSTART_EXCEL_MACOS.md` — macOS-specific quick start
- `docs/XLWINGS_ADDON_SETUP.md` — Add-in setup and troubleshooting
- `docs/TRAINING_RESULTS.md` — Model training metrics
- `docs/PREDICTION_TEST_RESULTS.md` — Sample predictions
- `docs/PROJECT_RESULTS.md` — Complete project summary
- `docs/AUTHORS.md` — Author and acknowledgements

## Troubleshooting

**Functions don't appear in xlwings dropdown:**
- Reinstall the add-in: `xlwings uninstall && xlwings install`
- Restart Excel completely.
- Check `xlwings.conf` is in the root folder.

**Excel listener won't run:**
- Ensure `src/` Python files exist and imports resolve.
- Check `artifacts/` contains model files.
- Verify the venv has all dependencies: `pip install -r requirements.txt`

**See:** `docs/XLWINGS_ADDON_SETUP.md` for more help.

## License

This project is part of an academic research effort. For details on usage and licensing, see individual file headers and documentation.
