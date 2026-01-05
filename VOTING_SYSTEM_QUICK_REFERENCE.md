# Voting Ensemble System - Quick Reference Guide

**Version:** 2.0  
**Date:** January 5, 2026  
**Status:** Production Ready

---

## Quick Start

### 1. Train Models
```bash
cd Backend
python train_voting_ensemble.py
```

### 2. Run Backend API
```bash
python main.py
# Runs on http://localhost:5000
```

### 3. Run Frontend
```bash
cd frontend
python -m http.server 8000
# Runs on http://localhost:8000
```

### 4. Access Application
Open browser: **http://localhost:8000**

---

## System Architecture

```
Patient Input (10 Medical Features)
    |
    V
KNN (77.59%) | RF (75.86%) | SVM (71.55%)
    |             |              |
    +--- Majority Voting ---+
              |
              V
        Final Decision
     + Confidence Score
```

---

## Algorithm Performance

---

## Algorithm Details

| Algorithm | Config | Accuracy | Type |
|-----------|--------|----------|------|
| **KNN** | K=3 | 77.59% | Instance-based |
| **Random Forest** | n=100, depth=15 | 75.86% | Ensemble trees |
| **SVM** | kernel=rbf, C=0.1 | 71.55% | Margin-based |
| **Ensemble** | Majority voting | **74.14%** | **Robust** |

---

## Voting Examples
```
KNN: YES (1)
RF:  YES (1)
SVM: NO  (0)
---
MAJORITY: 2 votes for YES -> RESULT: YES
Confidence: 66.67%
```

### Example 2: NO (No Disease)
```
KNN: NO  (0)
RF:  NO  (0)
SVM: YES (1)
---
MAJORITY: 2 votes for NO -> RESULT: NO
Confidence: 66.67%
```

### Example 3: Unanimous YES
```
KNN: YES (1)
RF:  YES (1)
SVM: YES (1)
---
RESULT: YES
Confidence: 100% (All algorithms agree)
```

### Example 4: Unanimous NO
```
KNN: NO (0)
RF:  NO (0)
SVM: NO (0)
---
RESULT: NO
Confidence: 100% (All algorithms agree)
```

---

## API Endpoints

### POST /predict
Single prediction with voting results
```json
Response: {
  "prediction": 1,
  "status": "Liver Disease Detected",
  "confidence": 100.0,
  "votes": {"knn": 1, "rf": 1, "svm": 1}
}
```

### POST /predict/{username}
Prediction with user history tracking

---

## Performance Metrics

**Voting Ensemble:**
- Accuracy: 74.14%
- Precision: 73.87%
- Recall: **98.80%** (High sensitivity for disease)
- F1-Score: 0.8454

**Test Results (145 samples):**
- Unanimous YES (3/3): 98 cases
- Majority YES (2/3): 22 cases
- Majority NO (1/3): 25 cases
- Unanimous NO (0/3): 0 cases

---

## Confidence Scoring

```
Confidence = (Agreeing Models / 3) × 100%

3/3 agree → 100% confidence (Unanimous)
2/3 agree → 66.67% confidence (Majority)
1/3 agree → 33.33% confidence (Minority)
```

---

## Running Everything

```bash
# Terminal 1: Backend
cd Backend
python main.py

# Terminal 2: Frontend
cd frontend
python -m http.server 8000
```

Access: **http://localhost:8000**

---

## Key Features Implemented

✓ Three ML algorithms (KNN, RF, SVM)
✓ Majority voting mechanism
✓ Confidence scoring
✓ FastAPI backend
✓ SQLite user database
✓ Prediction history tracking
✓ Responsive frontend
✓ User authentication

---

## Production Status

Status: **PRODUCTION READY**

Components:
- [x] Models trained and saved
- [x] Voting logic implemented
- [x] API integrated
- [x] Frontend updated
- [x] Database functional
- [x] Testing complete
- [x] Documentation done

---

## Next Steps

1. Deploy to production server
2. Monitor prediction accuracy
3. Collect user feedback
4. Retrain quarterly with new data
5. Consider weighted voting
6. Add more algorithms (optional)

---

Generated: January 5, 2026


1. **train_voting_ensemble.py** - Trains all 3 models and voting ensemble
2. **voting_ensemble_model.pkl** - Saved trained models
3. **main.py** - FastAPI backend with voting predictions
4. **test_voting_demo.py** - Demonstration and testing

---

## Key Performance

- **KNN**: 77.59%
- **Random Forest**: 75.86%
- **SVM**: 71.55%
- **Voting Ensemble**: 74.14% (Balanced & Robust)
- **Recall**: 98.80% (Catches disease cases)
- **Precision**: 73.87%

---

## Running Everything

```bash
# 1. Train models
python Backend/train_voting_ensemble.py

# 2. Run API (in separate terminal)
cd Backend
python main.py

# 3. Test the system (in another terminal)
python Backend/test_voting_demo.py
```

---

## API Usage

**Endpoint**: `POST /predict`

**Request**:
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

**Response**:
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

## Voting Logic Summary

```python
votes = [knn_prediction, rf_prediction, svm_prediction]

if sum(votes) >= 2:
    final_result = 1  # YES - Disease Detected
else:
    final_result = 0  # NO - No Disease

confidence = (number_of_agreeing_models / 3) * 100
```

---

## Project Status: COMPLETE

All requirements have been implemented and tested:
- [x] KNN algorithm trained
- [x] Random Forest algorithm trained
- [x] SVM algorithm trained
- [x] Voting system with majority voting
- [x] API integration
- [x] Test demonstrations
- [x] Documentation
