# PLPD

**PLPD** is a Python package for **data preprocessing, visualization and regression pipelines**.  
It provides tools to quickly explore, clean, and prepare datasets, as well as test multiple regression models to identify the best-performing one.

---

## Features

### DataEditor
- Inspect and preview columns and their unique values.
- Detect and handle potentially ordinal categorical values for manual ordering.
- Manage missing values with multiple options:
  - Mean imputation
  - Deleting rows or columns with missing values
  - Iterative imputation using `sklearn`’s `IterativeImputer`
- GUI-based interaction for assigning categories and previewing data.
- Generates visualizations of missing data with `missingno` and `matplotlib`.

### RegressionPipeline
- Try multiple regression models easily:
  - Linear Regression, Lasso, Ridge
  - Random Forest Regressor
  - XGBoost Regressor
  - Support Vector Regressor
- Add custom regressors with `.add_model()` or `.add_models()`.
- Automatically preprocess data (one-hot encoding, scaling) for regression.
- Evaluate models using cross-validation to find the best-performing regressor.
- Provides a simple `lazy_regression()` method for quick testing.

---

## Installation (editable mode)

1. Open a terminal in the **root folder** containing `setup.py`.
2. Create a clean conda environment (optional but recommended):

```bash
conda create -n plpd_env python=3.12
conda activate plpd_env

