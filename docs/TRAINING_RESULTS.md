# Kickstarter Success Prediction Model - Training Results

## Date
December 4, 2025

## Model Training Summary

### Dataset
- **Source:** `ks-projects-201801.csv`
- **Total Records:** 37,887 campaigns
- **Training Set:** 70% (26,520 records)
- **Validation Set:** 30% (11,367 records)

### Model Architecture
- **Framework:** TensorFlow/Keras
- **Model Type:** Deep Neural Network
- **Input Features:** 58 (after one-hot encoding of categorical variables)
- **Output:** Binary classification (Success/Failure probability)

### Training Configuration
- **Epochs:** 10
- **Batch Size:** 32
- **Optimizer:** Adam (default)
- **Loss Function:** Binary crossentropy
- **Metrics:** Accuracy, AUC

### Final Performance Metrics

| Metric | Training | Validation |
|--------|----------|-----------|
| **Accuracy** | 91.36% | 92.08% |
| **AUC (Area Under Curve)** | 0.9733 | 0.9780 |
| **Loss** | 0.2086 | 0.1942 |

### Epoch-by-Epoch Progress

| Epoch | Train Acc | Train AUC | Train Loss | Val Acc | Val AUC | Val Loss |
|-------|-----------|----------|-----------|---------|---------|----------|
| 1 | 79.12% | 0.8717 | 0.4493 | 84.90% | 0.9244 | 0.3491 |
| 2 | 85.58% | 0.9302 | 0.3368 | 87.20% | 0.9453 | 0.3118 |
| 3 | 87.21% | 0.9440 | 0.3023 | 88.61% | 0.9552 | 0.2685 |
| 4 | 88.57% | 0.9543 | 0.2740 | 89.41% | 0.9612 | 0.2514 |
| 5 | 89.44% | 0.9608 | 0.2530 | 89.98% | 0.9658 | 0.2373 |
| 6 | 90.05% | 0.9649 | 0.2396 | 91.36% | 0.9727 | 0.2112 |
| 7 | 90.53% | 0.9680 | 0.2287 | 91.52% | 0.9740 | 0.2054 |
| 8 | 90.78% | 0.9698 | 0.2224 | 91.75% | 0.9747 | 0.2024 |
| 9 | 91.06% | 0.9718 | 0.2146 | 91.83% | 0.9750 | 0.2016 |
| 10 | 91.36% | 0.9733 | 0.2086 | 92.08% | 0.9780 | 0.1942 |

### Model Artifacts Generated
- `kickstarter_model.keras` - Trained neural network model
- `scaler.pkl` - StandardScaler for feature normalization
- `feature_columns.json` - Feature column mappings and categorical encoding

### Key Findings
✅ **Strong Model Performance:** 92.08% validation accuracy indicates excellent predictive capability
✅ **High AUC Score:** 0.9780 AUC demonstrates strong discriminative power between successful and failed projects
✅ **No Overfitting:** Validation metrics are better than training metrics, indicating good generalization
✅ **Convergence:** Model converged smoothly with decreasing loss throughout training

### Feature Engineering Applied
- Temporal features extracted from dates (year, month, day)
- One-hot encoding for categorical features:
  - category
  - main_category
  - currency
  - country
- Feature normalization using StandardScaler
- Missing values imputation (usd_pledged mean strategy)

### Next Steps
1. ✅ Model trained and saved
2. ⏳ Excel integration via xlwings
3. ⏳ Deploy to production
4. ⏳ Create API endpoint for predictions

### Model Usage
```python
from model_pipeline import load_artifacts, predict_success_probability

# Load trained model
model, scaler, feature_columns = load_artifacts(Path("./artifacts"))

# Make predictions
probability = predict_success_probability(
    campaign_data, 
    model, 
    scaler, 
    feature_columns
)
```

### Environment
- Python Version: 3.9.6
- TensorFlow Version: 2.x
- Scikit-learn Version: Latest
- Pandas Version: Latest

---
**Status:** ✅ Training Complete and Successfully Saved

## Author

Mohamed SharafEldin  
Academic number: 202201849  
Academic email: 12422021653750@pg.cu.edu.eg

Under Supervision of:  
- Dr. Tarek Ali
  Faculty of Graduate Studies for Statistical Research
- Prof. Mervat Gheith
  Faculty of Graduate Studies for Statistical Research
