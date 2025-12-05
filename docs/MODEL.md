# Model Architecture

**Date:** February 2024

## Overview

Deep neural network trained on 37,887 Kickstarter campaigns to predict success probability.

## Architecture

**Framework:** TensorFlow/Keras

**Layers:**
- Input: 58 features
- Hidden layers with dropout regularization
- Output: Sigmoid (0-1 probability)

**Optimizer:** Adam  
**Loss:** Binary crossentropy  
**Metrics:** Accuracy, AUC

## Features

**Numerical:**
- goal, pledged, backers, usd_pledged

**Categorical (one-hot encoded):**
- category, main_category, currency, country

**Temporal (extracted from dates):**
- deadline_year, deadline_month
- launched_year, launched_month

## Training

- **Epochs:** 10
- **Batch Size:** 32
- **Train/Val Split:** 70/30
- **Data:** 37,887 campaigns

## Model Files

- `kickstarter_model.keras` — Trained model (463 KB)
- `scaler.pkl` — Feature scaler (10 KB)
- `feature_columns.json` — Feature names (5 KB)

Saved in `/artifacts/` folder.
