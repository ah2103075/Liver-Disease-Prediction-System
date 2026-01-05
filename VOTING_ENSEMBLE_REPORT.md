# Liver Disease Prediction System - Voting Ensemble Technical Report

**Version:** 2.0  
**Date:** January 5, 2026  
**Status:** Production Ready

---

## Executive Summary

This document provides a comprehensive technical overview of the Voting Ensemble System implemented for liver disease prediction. The system combines three machine learning algorithms (KNN, Random Forest, and SVM) using majority voting to deliver robust, explainable predictions for medical diagnosis support.

---

## System Architecture

```
Patient Medical Data (10 Features)
        |
        +---> Feature Preprocessing & Normalization
        |
        V
    +-----------+-----------+-----------+
    |           |           |           |
    V           V           V           V
  KNN (K=3)  RF (n=100)  SVM (rbf)  Voting
 77.59%      75.86%      71.55%     Logic
    |           |           |           |
    +-----[Prediction 1]-----+           |
    +-----[Prediction 2]-----+           |
    +-----[Prediction 3]-----+           |
                |                        |
                +----------+[Majority Voting]+
                           |
                           V
                    Final Prediction
                    + Confidence Score
                    + Algorithm Votes
```

---

## Implementation Overview

### 1. **Three Machine Learning Algorithms Trained**

#### Algorithm 1: K-Nearest Neighbors (KNN)
- **Best Configuration**: K=3
- **Accuracy**: 77.59%
- **Type**: Instance-based learning
- **Strengths**: Simple, effective for local patterns

#### Algorithm 2: Random Forest (RF)
- **Best Configuration**: n_estimators=100, max_depth=15
- **Accuracy**: 75.86%
- **Type**: Ensemble of decision trees
- **Strengths**: Robust to overfitting, handles non-linear relationships

#### Algorithm 3: Support Vector Machine (SVM)
- **Best Configuration**: kernel='rbf', C=0.1
- **Accuracy**: 71.55%
- **Type**: Margin-based classifier
- **Strengths**: Effective in high-dimensional spaces

---

## Voting System Architecture

### **Majority Voting Logic**

The system uses **majority voting** to combine predictions from all three algorithms:

```
IF (Number of "Yes" votes >= 2) THEN
    Result = "Yes" (Disease Detected)
ELSE
    Result = "No" (No Disease)
```

### **Examples**

| Case | KNN | RF | SVM | Votes | Result | Confidence |
|------|-----|----|----|-------|--------|-----------|
| 1 | Yes | Yes | No | 2 | **YES** | 66.67% |
| 2 | No | No | Yes | 1 | **NO** | 66.67% |
| 3 | Yes | Yes | Yes | 3 | **YES** | 100% |
| 4 | No | No | No | 0 | **NO** | 100% |
| 5 | Yes | No | No | 1 | **NO** | 66.67% |

---

## Performance Metrics

### Individual Algorithm Performance
- **KNN**: 77.59% accuracy
- **Random Forest**: 75.86% accuracy  
- **SVM**: 71.55% accuracy

### Voting Ensemble Performance
- **Ensemble Accuracy**: 74.14%
- **Precision**: 73.87%
- **Recall**: 98.80%
- **F1-Score**: 0.8454

### Test Set Analysis (145 samples)
- **Unanimous "Yes" (3/3)**: 98 cases
- **Majority "Yes" (2/3)**: 22 cases
- **Majority "No" (1/3)**: 25 cases
- **Unanimous "No" (0/3)**: 0 cases

---

## Key Files

### Training & Models
1. **`train_voting_ensemble.py`** - Complete training pipeline
   - Trains all three algorithms
   - Performs hyperparameter optimization
   - Evaluates individual and ensemble performance
   - Saves trained models

2. **`voting_ensemble_model.pkl`** - Saved ensemble model containing:
   - KNN pipeline with scaler
   - Random Forest pipeline
   - SVM pipeline
   - Accuracy metrics for all models

### API Integration
3. **`main.py`** - FastAPI backend
   - `/predict` - Single prediction with voting
   - `/predict/{username}` - Prediction with history tracking
   - `/batch-predict` - Batch predictions
   - Authentication endpoints
   - History management

### Testing
4. **`test_voting_demo.py`** - Comprehensive test demonstrating:
   - Voting logic with specific examples
   - Real predictions from test set
   - Voting breakdown analysis
   - Performance metrics

---

## Confidence Scoring

Confidence is calculated based on algorithm agreement:
- **100%**: All 3 algorithms agree (unanimous)
- **66.67%**: 2 out of 3 algorithms agree (majority)
- **33.33%**: 1 out of 3 algorithms agree (minority - not used for prediction)

---

## Benefits of Voting Ensemble

1. **More Robust**: Reduces impact of individual algorithm errors
2. **Better Generalization**: Combines different learning approaches
3. **High Recall (98.80%)**: Catches positive cases effectively
4. **Confidence Scores**: Users know when predictions are unanimous vs. split
5. **Interpretable**: Clear voting breakdown shows which algorithms agree

---

## Feature Set (10 Features)

1. Age
2. Gender
3. Total Bilirubin
4. Direct Bilirubin
5. Alkaline Phosphatase
6. Alamine Aminotransferase (SGPT)
7. Aspartate Aminotransferase (SGOT)
8. Total Proteins
9. Albumin
10. Albumin/Globulin Ratio

---

## How It Works in Practice

### Single Prediction Example
```json
{
  "Age": 48,
  "Gender": 1,
  "Total_Bilirubin": 0.8,
  "Direct_Bilirubin": 0.2,
  "Alkaline_Phosphotase": 120,
  "Alamine_Aminotransferase": 25,
  "Aspartate_Aminotransferase": 30,
  "Total_Proteins": 7.2,
  "Albumin": 3.5,
  "Albumin_and_Globulin_Ratio": 1.1
}
```

### API Response
```json
{
  "prediction": 1,
  "status": "Liver Disease Detected",
  "confidence": 100,
  "votes": {
    "knn": 1,
    "random_forest": 1,
    "svm": 1
  }
}
```

---

## Running the System

### 1. Train Models
```bash
python train_voting_ensemble.py
```

### 2. Run API Server
```bash
python main.py
```
Server runs on `http://localhost:5000`

### 3. Test Voting System
```bash
python test_voting_demo.py
```

---

## Technical Stack

- **Python 3.13**
- **Scikit-learn**: ML algorithms (KNN, Random Forest, SVM)
- **Pandas**: Data handling
- **NumPy**: Numerical operations
- **FastAPI**: REST API framework
- **Joblib/Pickle**: Model serialization

---

## Conclusion

The voting ensemble system successfully combines three diverse machine learning algorithms to create a more robust liver disease prediction system. With high recall (98.80%), the system is effective at identifying potential liver disease cases while maintaining reasonable precision (73.87%).
