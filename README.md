# 🫀 Liver Disease Prediction System

An advanced machine learning application that predicts liver disease risk using K-Nearest Neighbors (KNN) algorithm based on medical parameters.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Stack](#technical-stack)
- [Model Information](#model-information)
- [API Endpoints](#api-endpoints)
- [Validation Rules](#validation-rules)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Overview

This application provides a comprehensive solution for predicting liver disease risk using machine learning. It combines a powerful backend API with a modern, responsive frontend interface to deliver accurate medical predictions with 77.59% accuracy using the KNN algorithm.

**Target Users:**
- Medical professionals
- Patients seeking health screening
- Healthcare institutions
- Research organizations

## Features

### 🔬 Core Prediction Features
- **K-Nearest Neighbors Model**: Uses K=3 for optimal accuracy (77.59%)
- **10 Medical Parameters**: Analyzes key liver function indicators
- **Real-time Predictions**: Instant disease risk assessment
- **Confidence Scoring**: Shows prediction confidence levels
- **Disease Status**: Clear POSITIVE/NEGATIVE classification

### 📊 User Management
- **User Authentication**: Secure signup and login system
- **Email Validation**: Comprehensive email format validation
- **Password Security**: Minimum 4 character requirement
- **SQLite Database**: User account storage and persistence
- **Session Management**: Secure user sessions with tokens

### 📈 Prediction History
- **Full History Tracking**: All predictions saved with timestamps
- **Search and Filter**: Find predictions by date and status
- **Medical Parameters Display**: View all input parameters for each prediction
- **Delete Capability**: Remove individual predictions from history
- **Timestamp Tracking**: Automatic date and time recording

### 🎨 User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark/Light Theme**: Toggle between themes for comfort
- **Modern Styling**: Professional card designs and animations
- **Field Suggestions**: Autocomplete dropdown for frequently used values
- **Form Validation**: Real-time validation feedback with specific error messages
- **Prediction Result Display**: Clear presentation of prediction outcomes

### 🔐 Security Features
- **Form Validation**: Email format and password strength checks
- **Form Progression Blocking**: Prevents invalid form submission
- **Token-Based Authentication**: Secure API access with JWT tokens
- **CORS Support**: Cross-origin resource sharing enabled
- **Input Sanitization**: All inputs validated before processing

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Port 8000)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Home Page   │  │ Signup/Login │  │  Prediction  │     │
│  │   (index)    │  │   Pages      │  │   Pages      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                 │              │
│         └──────────────────┼─────────────────┘              │
│                            │                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          HTML5 + CSS3 + JavaScript                  │  │
│  │  - Responsive Design  - Form Validation             │  │
│  │  - Dark/Light Theme   - Field Suggestions           │  │
│  │  - Smooth Animations  - Real-time Feedback          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────┬──┘
                         │ HTTP REST API                   │
                         │ (JSON)                          │
    ┌────────────────────▼────────────────────────────────▼──┐
    │               BACKEND (Port 5000)                      │
    │           FastAPI + Uvicorn                            │
    │  ┌──────────────────────────────────────────────────┐  │
    │  │  API Endpoints                                   │  │
    │  │  /predict      - Make predictions               │  │
    │  │  /signup       - User registration              │  │
    │  │  /login        - User authentication            │  │
    │  │  /history      - Get prediction history         │  │
    │  └──────────────────────────────────────────────────┘  │
    │                       │                                 │
    │  ┌────────────────────▼───────────────────────────┐   │
    │  │  KNN Model (scikit-learn)                      │   │
    │  │  - 10 Medical Parameters                       │   │
    │  │  - K=3 Neighbors                              │   │
    │  │  - 77.59% Accuracy                            │   │
    │  │  - Binary Classification (0/1)                │   │
    │  └────────────────────┬───────────────────────────┘   │
    │                       │                                 │
    │  ┌────────────────────▼───────────────────────────┐   │
    │  │  SQLite Database                               │   │
    │  │  - User Accounts                              │   │
    │  │  - Prediction History                         │   │
    │  │  - Training Data                              │   │
    │  └────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Windows/Mac/Linux operating system

### Backend Setup

1. **Navigate to Backend Directory**
```bash
cd Backend
```

2. **Install Python Dependencies**
```bash
pip install fastapi uvicorn scikit-learn pandas numpy
```

3. **Train the KNN Model** (if needed)
```bash
python train_knn_optimized.py
```

4. **Start the Backend Server**
```bash
python main.py
```
Server will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to Frontend Directory**
```bash
cd frontend
```

2. **Start the Frontend Server**

**Windows (PowerShell):**
```powershell
python -m http.server 8000
```

**Mac/Linux (Bash):**
```bash
python3 -m http.server 8000
```

Server will run on `http://localhost:8000`

### Quick Start (Automated)

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
bash start.sh
```

## Usage

### 1. Access the Application
- Open your web browser
- Navigate to `http://localhost:8000`
- You'll see the welcome page

### 2. Create an Account
- Click "Create Account" button
- Fill in the signup form:
  - **Full Name**: Your complete name
  - **Email**: Valid email format (must contain @ and .)
  - **Username**: 3-20 alphanumeric characters with underscores/hyphens
  - **Password**: Minimum 4 characters
  - **Confirm Password**: Match the password field
- Click "Sign Up"
- Redirect to login page automatically

### 3. Login
- Enter your username and password
- Click "Login"
- Access the prediction page

### 4. Make a Prediction
- Enter all 10 medical parameters:
  1. **Age** (years): Patient age in years
  2. **Gender**: Male (1) or Female (0)
  3. **Total Bilirubin** (mg/dL): Total bilirubin level
  4. **Direct Bilirubin** (mg/dL): Direct bilirubin level
  5. **Alkaline Phosphatase** (U/L): Enzyme level
  6. **Alamine Aminotransferase** (U/L): ALT enzyme level
  7. **Aspartate Aminotransferase** (U/L): AST enzyme level
  8. **Total Proteins** (g/dL): Total protein level
  9. **Albumin** (g/dL): Albumin level
  10. **Albumin-Globulin Ratio**: AG ratio value

- Click "Get Prediction"
- View the result:
  - **POSITIVE**: Disease detected (Class 1)
  - **NEGATIVE**: No disease detected (Class 0)
  - **Confidence**: Prediction confidence percentage

### 5. View History
- Click "View History" button
- See all your previous predictions
- Each record shows:
  - Prediction result (POSITIVE/NEGATIVE)
  - Timestamp
  - All input parameters
- Delete individual predictions with delete button
- Clear all history with "Clear History" button

### 6. Toggle Theme
- Click the moon/sun icon in the top right
- Switch between dark and light themes
- Preference is saved locally

## Project Structure

```
Liver-Disease-Prediction-System/
├── README.md                              # Project documentation
├── SYSTEM_STATUS.md                       # System status report
├── PROJECT_REPORT.md                      # Detailed project report
│
├── start.bat                              # Windows startup script
├── start.ps1                              # PowerShell startup script
├── start.sh                               # Linux/Mac startup script
│
├── Backend/                               # Backend API
│   ├── main.py                            # FastAPI application
│   ├── database.py                        # Database operations
│   ├── train_knn_optimized.py            # KNN model training
│   ├── Indian Liver Patient Dataset.csv  # Training data
│   ├── __pycache__/                      # Python cache
│   └── data/                             # Model and data files
│
└── frontend/                              # Frontend application
    ├── index.html                         # Welcome/home page
    ├── signup.html                        # User registration page
    ├── signup.js                          # Registration validation
    ├── login.html                         # User login page
    ├── login.js                           # Login validation
    ├── access.html                        # Prediction page
    ├── access.js                          # Prediction logic
    ├── history.html                       # Prediction history page
    ├── history.js                         # History management
    ├── style.css                          # Application styling
    ├── theme.js                           # Dark/light theme toggle
    └── README.md                          # Frontend documentation
```

## Technical Stack

### Backend
- **Framework**: FastAPI (Python)
- **Server**: Uvicorn (ASGI)
- **ML Library**: scikit-learn 1.8.0
- **Data Processing**: pandas, numpy
- **Database**: SQLite
- **Authentication**: JWT tokens

### Frontend
- **Markup**: HTML5
- **Styling**: CSS3 with variables and animations
- **Scripting**: Vanilla JavaScript (ES6+)
- **Theme System**: CSS custom properties (--primary-color, --bg-primary, etc.)
- **Storage**: LocalStorage API
- **HTTP Client**: Fetch API

### Build & Deployment
- **Backend Server**: Python HTTP Server
- **Frontend Server**: Python HTTP Server
- **Port Configuration**: Backend 5000, Frontend 8000

## Model Information

### KNN Algorithm Details
```
Model Type:           K-Nearest Neighbors (KNN)
Training Dataset:     Indian Liver Patient Dataset (ILPD)
Total Samples:        583 patients
Features:             10 medical parameters
Target Variable:      Binary (0 = Negative, 1 = Positive)
K Value:              3 neighbors
Accuracy:             77.59%
Classification:       Binary (Disease Present / Absent)
```

### Medical Parameters

| Parameter | Unit | Range | Description |
|-----------|------|-------|-------------|
| Age | years | 0-120 | Patient age |
| Gender | 0/1 | M/F | Male=1, Female=0 |
| Total Bilirubin | mg/dL | 0.1-75 | Total bilirubin level |
| Direct Bilirubin | mg/dL | 0.1-19.3 | Direct bilirubin level |
| Alkaline Phosphatase | U/L | 23-2110 | ALP enzyme level |
| Alamine Aminotransferase | U/L | 10-2000 | ALT enzyme level |
| Aspartate Aminotransferase | U/L | 10-4929 | AST enzyme level |
| Total Proteins | g/dL | 4.0-9.0 | Total protein level |
| Albumin | g/dL | 1.0-7.5 | Albumin level |
| Albumin-Globulin Ratio | ratio | 0.2-2.8 | AG ratio |

## API Endpoints

### 1. Make Prediction
```
POST /predict
Content-Type: application/json

Request Body:
{
    "Age": 25,
    "Gender": 1,
    "Total_Bilirubin": 0.7,
    "Direct_Bilirubin": 0.1,
    "Alkaline_Phosphotase": 225,
    "Alamine_Aminotransferase": 14,
    "Aspartate_Aminotransferase": 4,
    "Total_Proteins": 6.1,
    "Albumin": 3.5,
    "Albumin_and_Globulin_Ratio": 0.6
}

Response (Success - 200):
{
    "prediction": 1,
    "status": "POSITIVE - Disease Detected",
    "confidence": 100.0,
    "message": "Disease Present"
}
```

### 2. User Signup
```
POST /signup
Content-Type: application/json

Request Body:
{
    "username": "john_doe",
    "password": "password123",
    "email": "john@example.com",
    "full_name": "John Doe"
}

Response (Success - 201):
{
    "message": "User created successfully",
    "access_token": "eyJhbGc...",
    "token_type": "bearer"
}
```

### 3. User Login
```
POST /login
Content-Type: application/json

Request Body:
{
    "username": "john_doe",
    "password": "password123"
}

Response (Success - 200):
{
    "message": "Login successful",
    "access_token": "eyJhbGc...",
    "token_type": "bearer"
}
```

## Validation Rules

### Email Validation
- ✅ Must contain `@` symbol
- ✅ Must contain `.` (dot) after `@`
- ✅ Local part: 1-64 characters [a-zA-Z0-9._+-]
- ✅ Domain: 1-255 characters (each label alphanumeric + hyphens)
- ✅ TLD: Minimum 2 letters (alphabetic only)
- ✅ Supports multi-level domains (e.g., student.ruet.ac.bd)

### Password Validation
- ✅ Minimum 4 characters required
- ✅ No maximum limit
- ✅ No character restrictions (supports all characters)
- ✅ Case-insensitive

### Username Validation
- ✅ 3-20 characters
- ✅ Alphanumeric characters, underscores, hyphens allowed
- ✅ No spaces or special characters except _ and -

### Full Name Validation
- ✅ Minimum 2 characters
- ✅ Letters, spaces, hyphens, apostrophes allowed
- ✅ No numbers or special characters

### Form Progression
- ✅ Password field only accessible when email is valid
- ✅ Cannot skip or manually focus on disabled fields
- ✅ Form submission blocked until all validations pass
- ✅ Real-time feedback on validation status

## Troubleshooting

### Backend Server Issues

**Error: Port 5000 already in use**
```bash
# Find process using port 5000 and kill it
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :5000
kill -9 <PID>
```

**Error: ModuleNotFoundError (scikit-learn, pandas, numpy)**
```bash
pip install scikit-learn pandas numpy
```

**Error: Database file not found**
- The database is created automatically on first run
- Check Backend/data/ directory for sqlite.db

### Frontend Server Issues

**Error: Port 8000 already in use**
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8000
kill -9 <PID>
```

**Page not loading / CORS errors**
- Ensure both servers are running
- Backend on http://localhost:5000
- Frontend on http://localhost:8000
- Check browser console for specific errors

### Prediction Issues

**Error: Empty or invalid medical parameters**
- All 10 fields must have valid numeric values
- Age must be 0-120
- Other values should be within expected medical ranges

**Error: API connection failed**
- Check if backend server is running
- Verify ports (5000 for backend, 8000 for frontend)
- Check browser console (F12) for detailed errors

### Database Issues

**Lost prediction history**
- Check if cookies/localStorage are enabled
- Try clearing browser cache
- Ensure you're logged into the same account
- History is per-user and stored in backend database

## Future Enhancements

### Planned Features
- [ ] Multiple ML models (Random Forest, SVM, Neural Networks)
- [ ] Model comparison and accuracy metrics
- [ ] Advanced filtering and search in history
- [ ] Export predictions to PDF/CSV
- [ ] Doctor/patient role management
- [ ] Data visualization and charts
- [ ] Mobile application (iOS/Android)
- [ ] Email notifications for predictions
- [ ] User profile management
- [ ] Password reset functionality
- [ ] Two-factor authentication (2FA)
- [ ] Admin dashboard and analytics
- [ ] Batch prediction processing
- [ ] API rate limiting and authentication
- [ ] Database optimization and indexing

### Performance Improvements
- [ ] Implement caching for predictions
- [ ] Database query optimization
- [ ] Frontend bundle optimization
- [ ] Progressive Web App (PWA) support
- [ ] Image and asset compression

## Support & Contact

For issues, suggestions, or contributions:
- Check the troubleshooting section
- Review system status in SYSTEM_STATUS.md
- See detailed report in PROJECT_REPORT.md

## License

This project is provided as-is for educational and medical research purposes.

## Version History

**v1.0.0** (December 30, 2025)
- Initial release
- KNN model with 77.59% accuracy
- User authentication system
- Prediction history tracking
- Dark/light theme support
- Responsive design

---

**Last Updated**: December 30, 2025
