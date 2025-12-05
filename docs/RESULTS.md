# Training & Test Results

**Date:** March 2024

## Final Performance

| Metric | Train | Validation |
|--------|-------|-----------|
| **Accuracy** | 91.36% | 92.08% ✅ |
| **AUC** | 0.9733 | 0.9780 ✅ |
| **Loss** | 0.2086 | 0.1942 |

## Epoch Progress

| Epoch | Train Acc | Val Acc | Train AUC | Val AUC |
|-------|-----------|---------|-----------|---------|
| 1 | 79.12% | 84.90% | 0.8717 | 0.9244 |
| 2 | 85.58% | 87.20% | 0.9302 | 0.9453 |
| 3 | 87.21% | 88.61% | 0.9440 | 0.9552 |
| 4 | 88.57% | 89.41% | 0.9543 | 0.9612 |
| 5 | 89.44% | 89.98% | 0.9608 | 0.9658 |
| 6 | 90.05% | 91.36% | 0.9649 | 0.9727 |
| 7 | 90.53% | 91.52% | 0.9680 | 0.9740 |
| 8 | 90.78% | 91.75% | 0.9698 | 0.9747 |
| 9 | 91.06% | 91.83% | 0.9718 | 0.9750 |
| 10 | 91.36% | 92.08% | 0.9733 | 0.9780 |

## Test Predictions

**Campaign 1** (Well-funded):
- Input: goal=50000, pledged=75000 (150%)
- Prediction: 99.99% success ✅

**Campaign 2** (Underfunded):
- Input: goal=100000, pledged=50000 (50%)
- Prediction: 0.02% success ✅

**Campaign 3** (Partial):
- Input: goal=75000, pledged=75000 (100%)
- Prediction: 75.93% success ✅

## Key Findings

✅ No overfitting (validation > training metrics)  
✅ Smooth convergence across epochs  
✅ Excellent AUC (0.9780) shows strong discrimination  
✅ Model generalizes well to unseen data
