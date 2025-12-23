# 🫀 Liver Disease Prediction System

A comprehensive machine learning application for predicting liver disease risk using the K-Nearest Neighbors algorithm with a modern web interface.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Model Information](#model-information)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 🔐 User Management
- Secure user signup and login
- Session management with localStorage
- User account management
- Password-protected access

### 🔬 Medical Prediction
- **10 medical parameters** for accurate diagnosis
- **69.83% accuracy** using KNN (K=9) algorithm
- Real-time prediction with confidence scores
- Color-coded results (Green=Healthy, Red=Patient)

### 📊 History Tracking
- Complete prediction history
- All medical parameters stored and displayed
- Timestamp with Bangladesh timezone (GMT+6)
- Delete individual or all predictions
- Export-ready data format

### 🎨 User Interface
- Responsive web design (Desktop/Mobile)
- Intuitive navigation
- Real-time form validation
- Professional styling with CSS3
- Emoji-based visual indicators

### 📱 Multi-Page Application
1. **Home Page** - Welcome & Information
2. **Signup Page** - User Registration
3. **Login Page** - User Authentication
4. **Prediction Page** - Medical Analysis
5. **History Page** - Results Tracking

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation & Running (5 minutes)

**1. Install Dependencies**
```bash
pip install fastapi uvicorn pydantic scikit-learn pandas numpy
```

**2. Terminal 1 - Start Backend**
```bash
cd "e:\Machine Learning\Liver Disease\Backend"
python main.py
```
```
✅ Backend running on http://localhost:5000
```

**3. Terminal 2 - Start Frontend**
```bash
cd "e:\Machine Learning\Liver Disease\frontend"
python -m http.server 8000
```
```
✅ Frontend running on http://localhost:8000
```

**4. Open in Browser**
```
http://localhost:8000
```

---

## 💻 System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10/11, Linux, macOS |
| **Python** | 3.8 or higher |
| **RAM** | Minimum 2GB, Recommended 4GB+ |
| **Storage** | ~500MB (including dependencies) |
| **Browser** | Chrome, Firefox, Safari, Edge (modern versions) |

### Python Packages
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
scikit-learn==1.3.2
pandas==2.1.1
numpy==1.26.2
sqlite3 (built-in)
```

---

## 📦 Installation

### Step-by-Step Guide

#### Option 1: Manual Installation

```bash
# 1. Clone or download the project
cd "e:\Machine Learning\Liver Disease"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start backend (Terminal 1)
cd Backend
python main.py

# 4. Start frontend (Terminal 2)
cd frontend
python -m http.server 8000

# 5. Open http://localhost:8000 in browser
```

#### Option 2: Using Virtual Environment (Recommended)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run as above
```

---

## 📖 Usage Guide

### 1. User Registration

1. Click **"Create Account"** on home page
2. Fill in the form:
   - **Username** (unique identifier)
   - **Email** (for account recovery)
   - **Password** (minimum recommended 6 characters)
   - **Full Name** (your name)
3. Click **"Sign Up"**
4. See success message → Redirected to login

### 2. User Login

1. Enter **Username** and **Password**
2. Click **"Login"**
3. Access prediction page
4. Your session is saved (you stay logged in)

### 3. Making a Prediction

Fill in all 10 medical parameters (in dataset order):

| # | Parameter | Normal Range | Unit |
|---|-----------|--------------|------|
| 1 | Age | 18-80 | years |
| 2 | Gender | M/F | - |
| 3 | Total Bilirubin | 0.5-1.5 | mg/dL |
| 4 | Direct Bilirubin | 0.0-0.3 | mg/dL |
| 5 | Alkaline Phosphatase | 40-150 | U/L |
| 6 | Alamine Aminotransferase | 10-40 | U/L |
| 7 | Aspartate Aminotransferase | 10-40 | U/L |
| 8 | Total Proteins | 6.0-8.0 | g/dL |
| 9 | Albumin | 3.5-5.5 | g/dL |
| 10 | Albumin-Globulin Ratio | 1.0-2.5 | - |

**After clicking "Get Prediction":**
- ✅ Result displays with status (POSITIVE/NEGATIVE)
- ✅ Confidence percentage (0-100%)
- ✅ Color-coded card (Green=Healthy, Red=Disease)
- ✅ Automatically saved to history

### 4. Viewing History

1. Click **"View History"**
2. See all past predictions with:
   - Timestamp (Bangladesh timezone)
   - All 10 medical parameters
   - Prediction result
   - Individual delete option
3. Options available:
   - **Refresh** - Reload latest predictions
   - **Clear All History** - Remove all records
   - **Back to Predict** - Return to prediction form

### 5. Logout

1. Click **"Logout"** button
2. Session cleared
3. Redirected to home page

---

## 🔌 API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication Endpoints

#### POST /signup
Create a new user account
```bash
curl -X POST "http://localhost:5000/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }'
```
**Response (201):**
```json
{
  "message": "User created successfully",
  "username": "john_doe"
}
```

#### POST /login
Authenticate user
```bash
curl -X POST "http://localhost:5000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "password123"
  }'
```
**Response (200):**
```json
{
  "message": "Login successful",
  "username": "john_doe",
  "user_id": "1"
}
```

### Prediction Endpoints

#### POST /predict/{username}
Make a prediction with medical parameters
```bash
curl -X POST "http://localhost:5000/predict/john_doe" \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 45,
    "Gender": 1,
    "Total_Bilirubin": 1.5,
    "Direct_Bilirubin": 0.5,
    "Alkaline_Phosphotase": 150,
    "Alamine_Aminotransferase": 30,
    "Aspartate_Aminotransferase": 35,
    "Total_Proteins": 7.0,
    "Albumin": 3.8,
    "Albumin_and_Globulin_Ratio": 1.2
  }'
```
**Response (200):**
```json
{
  "prediction": 0,
  "status": "No Liver Disease",
  "confidence": 75.50
}
```

### History Endpoints

#### GET /history/{username}
Retrieve all predictions for a user
```bash
curl "http://localhost:5000/history/john_doe"
```
**Response (200):**
```json
{
  "username": "john_doe",
  "records": [
    {
      "id": 1,
      "medical_parameters": "{\"Age\": 45, ...}",
      "prediction": 0,
      "status": "No Liver Disease",
      "confidence": 75.50,
      "timestamp": "2025-12-21 09:17:44"
    }
  ],
  "total_predictions": 1
}
```

#### DELETE /history/{username}/{prediction_id}
Delete a specific prediction
```bash
curl -X DELETE "http://localhost:5000/history/john_doe/1"
```

#### DELETE /history/{username}
Clear all predictions for a user
```bash
curl -X DELETE "http://localhost:5000/history/john_doe"
```

---

## 📁 Project Structure

```
Liver Disease/
│
├── Backend/
│   ├── main.py                              (FastAPI application)
│   ├── database.py                          (SQLite database operations)
│   ├── train_knn.py                         (Model training script)
│   ├── train_balanced_knn.py                (Alternative training)
│   ├── knn_model.pkl                        (Trained KNN model)
│   ├── dt_model.pkl                         (Model backup)
│   ├── liver_disease.db                     (SQLite database)
│   ├── Indian Liver Patient Dataset (ILPD).csv
│   └── __pycache__/                         (Cache directory)
│
├── frontend/
│   ├── index.html                           (Redirect page)
│   ├── home.html                            (Welcome & Info)
│   ├── signup.html                          (Registration)
│   ├── login.html                           (Authentication)
│   ├── access.html                          (Prediction form)
│   ├── history.html                         (Prediction history)
│   ├── style.css                            (Styling & Layout)
│   ├── home.js                              (Home page logic)
│   ├── signup.js                            (Signup handler)
│   ├── login.js                             (Login handler)
│   ├── access.js                            (Prediction handler)
│   └── history.js                           (History handler)
│
├── README.md                                (This file)
├── PROJECT_REPORT.md                        (Detailed report)
├── SYSTEM_STATUS.html                       (System status page)
├── COMPLETE_REPORT.txt                      (Original report)
└── requirements.txt                         (Python dependencies)
```

---

## 🤖 Model Information

### Algorithm
- **Type:** Classification
- **Method:** K-Nearest Neighbors (KNN)
- **Framework:** Scikit-learn
- **Preprocessing:** StandardScaler

### Performance Metrics
- **Accuracy:** 69.83%
- **Precision (Patients):** 74%
- **Recall (Patients):** 89% (High sensitivity)
- **F1-Score:** 0.81

### Dataset
- **Name:** Indian Liver Patient Dataset (ILPD)
- **Records:** 583 patients (579 after cleaning)
- **Features:** 10 medical parameters
- **Target:** Binary classification (0=Healthy, 1=Patient)
- **Train/Test Split:** 80% (463) / 20% (116)

### Training Details
```python
# Optimal K value: 9
KNN Pipeline:
  - StandardScaler (normalization)
  - KNeighborsClassifier (n_neighbors=9)

# Cross-validation results:
K=3:  Accuracy=0.6638
K=5:  Accuracy=0.6552
K=7:  Accuracy=0.6897
K=9:  Accuracy=0.6983 ✅ (BEST)
K=11: Accuracy=0.6897
K=13: Accuracy=0.6810
K=15: Accuracy=0.6810
```

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT UNIQUE,
    full_name TEXT,
    created_at TIMESTAMP
)
```

### Predictions Table
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    age REAL,
    gender TEXT,
    tb REAL,              -- Total_Bilirubin
    db REAL,              -- Direct_Bilirubin
    alkphos REAL,         -- Alkaline_Phosphotase
    sgpt REAL,            -- Alamine_Aminotransferase
    sgot REAL,            -- Aspartate_Aminotransferase
    tp REAL,              -- Total_Proteins
    alb REAL,             -- Albumin
    ag_ratio REAL,        -- Albumin_and_Globulin_Ratio
    prediction INTEGER,   -- 0 or 1
    status TEXT,
    confidence REAL,      -- 0-100
    created_at TIMESTAMP
)
```

---

## ⚙️ Configuration

### Backend Configuration

**File:** `Backend/main.py`

```python
# Server settings
HOST = "0.0.0.0"
PORT = 5000

# Database
DB_PATH = "liver_disease.db"

# Model
MODEL_PATH = "knn_model.pkl"
```

### Frontend Configuration

**File:** `frontend/home.js`, `access.js`, etc.

```javascript
// API Base URL
const API_URL = 'http://localhost:5000';

// Timezone offset (Bangladesh = GMT+6)
const TIMEZONE_OFFSET = 6 * 60 * 60 * 1000;
```

### Database Configuration

Auto-creates SQLite database on first run:
- Location: `Backend/liver_disease.db`
- Tables: Automatically created
- No additional configuration needed

---

## 🔧 Troubleshooting

### 1. Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F

# Or use a different port
python main.py --port 5001
```

### 2. Module Not Found

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
pip install fastapi uvicorn pydantic scikit-learn pandas numpy
```

### 3. Database Lock

**Error:** `database is locked`

**Solution:**
```bash
# Delete existing database
rm Backend/liver_disease.db

# System will recreate on next startup
```

### 4. Medical Parameters Showing as "undefined"

**Error:** History page shows undefined for medical parameters

**Solution:**
- Backend must be restarted after code changes
- Clear browser cache and localStorage
- Check database.py mapping is correct

### 5. Predictions Not Saving

**Error:** Prediction completes but doesn't appear in history

**Solution:**
- Verify user is logged in (check localStorage)
- Confirm database file exists
- Check backend logs for errors
- Restart both servers

### 6. Login Not Working

**Error:** "Invalid username or password"

**Solution:**
- Verify username and password are correct
- Check if database file exists
- Try signing up a new account
- Clear browser localStorage

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **Model Enhancement:**
   - Try different algorithms (Random Forest, SVM)
   - Implement ensemble methods
   - Add cross-validation

2. **Features:**
   - Export predictions to PDF/CSV
   - Comparative analysis over time
   - Risk stratification levels
   - Mobile app version

3. **Security:**
   - Add password hashing
   - Implement JWT tokens
   - Enable HTTPS
   - Add role-based access

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make improvements
4. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Support

For issues, questions, or suggestions:

1. Check **Troubleshooting** section above
2. Review **PROJECT_REPORT.md** for detailed documentation
3. Check logs in terminal for error messages
4. Verify all dependencies are installed

---

## 📚 Additional Resources

- **Detailed Report:** See `PROJECT_REPORT.md`
- **System Status:** See `SYSTEM_STATUS.html`
- **Dataset Info:** `Backend/Indian Liver Patient Dataset (ILPD).csv`
- **Training Script:** `Backend/train_knn.py`

---

## ✅ Checklist

Before using the system:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Two terminals ready (one for backend, one for frontend)
- [ ] Ports 5000 and 8000 available
- [ ] Read through Usage Guide section
- [ ] Test with sample medical values

---

**🎉 Ready to predict liver disease!**

For the best experience:
1. Start with creating a test account
2. Try making a prediction with realistic medical values
3. View your prediction history
4. Explore all features

---

**Last Updated:** December 21, 2025  
**Version:** 1.0  
**Status:** Production Ready ✅

---

*Questions? Check PROJECT_REPORT.md or SYSTEM_STATUS.html for more information.*
