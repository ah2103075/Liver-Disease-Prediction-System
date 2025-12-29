from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import pickle
import json
from datetime import datetime
import sqlite3
from database import init_db, add_user, get_user, user_exists, add_prediction, get_user_predictions, delete_prediction, clear_user_history
import uvicorn
import pickle
import numpy as np
import os
from typing import List, Optional
from datetime import datetime
from database import init_db, add_user, get_user, user_exists, add_prediction, get_user_predictions, delete_prediction, clear_user_history

app = FastAPI(title="Liver Disease Prediction API", version="1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Load the model (pipeline with scaler + classifier)
# Using optimized KNN model with K=3 for maximum accuracy (77.59%)
model_path = os.path.join(os.path.dirname(__file__), 'knn_best_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)  # This is a Pipeline with scaler and KNN classifier (K=3)

# Feature names for the liver disease model (matching dataset column order)
FEATURE_NAMES = [
    'Age',
    'Gender',
    'Total_Bilirubin',
    'Direct_Bilirubin',
    'Alkaline_Phosphotase',
    'Alamine_Aminotransferase',
    'Aspartate_Aminotransferase',
    'Total_Proteins',
    'Albumin',
    'Albumin_and_Globulin_Ratio'
]

# Pydantic models for request/response
class PredictionRequest(BaseModel):
    Age: float
    Gender: float
    Total_Bilirubin: float
    Direct_Bilirubin: float
    Alkaline_Phosphotase: float
    Alamine_Aminotransferase: float
    Aspartate_Aminotransferase: float
    Total_Proteins: float
    Albumin: float
    Albumin_and_Globulin_Ratio: float

class PredictionResponse(BaseModel):
    prediction: int
    status: str
    confidence: Optional[float] = None

class BatchPredictionRequest(BaseModel):
    records: List[PredictionRequest]

class BatchPredictionResponse(BaseModel):
    total_records: int
    results: List[dict]

class SignUpRequest(BaseModel):
    username: str
    password: str
    email: str
    full_name: str

class LoginRequest(BaseModel):
    username: str
    password: str

class SignUpResponse(BaseModel):
    message: str
    username: str

class LoginResponse(BaseModel):
    message: str
    username: str
    user_id: str

class HistoryRecord(BaseModel):
    age: float
    gender: str
    prediction: int
    status: str
    confidence: float
    timestamp: str

class HistoryResponse(BaseModel):
    username: str
    records: List[dict]
    total_predictions: int

@app.get("/")
def home():
    return {
        'message': 'Liver Disease Prediction API',
        'version': '1.0',
        'endpoints': {
            'predict': '/predict (POST)',
            'batch-predict': '/batch-predict (POST)',
            'features': '/features (GET)',
            'signup': '/signup (POST)',
            'login': '/login (POST)',
            'history': '/history/<username> (GET)',
            'docs': '/docs'
        }
    }

# Authentication Endpoints
@app.post("/signup", response_model=SignUpResponse)
def signup(request: SignUpRequest):
    if user_exists(request.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if add_user(request.username, request.password, request.email, request.full_name):
        return SignUpResponse(message="Account created successfully", username=request.username)
    else:
        raise HTTPException(status_code=400, detail="Email already exists")

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user = get_user(request.username)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if user['password'] != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return LoginResponse(
        message="Login successful",
        username=request.username,
        user_id=str(user['id'])
    )

@app.get("/history/{username}", response_model=HistoryResponse)
def get_history(username: str):
    user = get_user(username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    predictions = get_user_predictions(user['id'])
    
    # Format for response
    records = []
    for pred in predictions:
        records.append({
            'id': pred['id'],
            'medical_parameters': pred['medical_parameters'],
            'prediction': pred['prediction'],
            'status': pred['status'],
            'confidence': pred['confidence'],
            'timestamp': pred['timestamp']
        })
    
    return HistoryResponse(
        username=username,
        records=records,
        total_predictions=len(records)
    )

@app.delete("/history/{username}/{prediction_id}")
def delete_single_prediction(username: str, prediction_id: int):
    user = get_user(username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if delete_prediction(prediction_id, user['id']):
        return {'message': 'Prediction deleted successfully'}
    else:
        raise HTTPException(status_code=400, detail="Failed to delete prediction")

@app.delete("/history/{username}")
def clear_history(username: str):
    user = get_user(username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if clear_user_history(user['id']):
        return {'message': 'History cleared successfully'}
    else:
        raise HTTPException(status_code=400, detail="Failed to clear history")

@app.get("/features")
def get_features():
    return {
        'features': FEATURE_NAMES,
        'total_features': len(FEATURE_NAMES)
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        # Extract features in the correct order
        features = [
            request.Age,
            request.Gender,
            request.Total_Bilirubin,
            request.Direct_Bilirubin,
            request.Alkaline_Phosphotase,
            request.Alamine_Aminotransferase,
            request.Aspartate_Aminotransferase,
            request.Total_Proteins,
            request.Albumin,
            request.Albumin_and_Globulin_Ratio
        ]
        
        # Convert to numpy array and reshape for prediction
        input_data = np.array(features).reshape(1, -1)
        
        # Make prediction (scaler is applied automatically by the pipeline)
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0] if hasattr(model, 'predict_proba') else None
        
        result = {
            'prediction': int(prediction),
            'status': 'Liver Disease Detected' if prediction == 1 else 'No Liver Disease',
        }
        
        if probability is not None:
            result['confidence'] = float(max(probability)) * 100
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/{username}")
def predict_with_history(username: str, request: PredictionRequest):
    try:
        user = get_user(username)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Extract features in the correct order (matching dataset)
        features = [
            request.Age,
            request.Gender,
            request.Total_Bilirubin,
            request.Direct_Bilirubin,
            request.Alkaline_Phosphotase,
            request.Alamine_Aminotransferase,
            request.Aspartate_Aminotransferase,
            request.Total_Proteins,
            request.Albumin,
            request.Albumin_and_Globulin_Ratio
        ]
        
        # Convert to numpy array and reshape for prediction
        input_data = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0] if hasattr(model, 'predict_proba') else None
        
        result = {
            'prediction': int(prediction),
            'status': 'Liver Disease Detected' if prediction == 1 else 'No Liver Disease',
        }
        
        if probability is not None:
            result['confidence'] = float(max(probability)) * 100
        else:
            result['confidence'] = 0.0
        
        # Add to database history
        add_prediction(
            user_id=user['id'],
            age=request.Age,
            gender='Male' if request.Gender == 1 else 'Female',
            tb=request.Total_Bilirubin,
            db=request.Direct_Bilirubin,
            alkphos=request.Alkaline_Phosphotase,
            sgpt=request.Alamine_Aminotransferase,
            sgot=request.Aspartate_Aminotransferase,
            tp=request.Total_Proteins,
            alb=request.Albumin,
            ag_ratio=request.Albumin_and_Globulin_Ratio,
            prediction=int(prediction),
            status=result['status'],
            confidence=result['confidence']
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-predict", response_model=BatchPredictionResponse)
def batch_predict(request: BatchPredictionRequest):
    try:
        results = []
        
        for idx, record in enumerate(request.records):
            features = [
                record.Age,
                record.Gender,
                record.Total_Bilirubin,
                record.Direct_Bilirubin,
                record.Alkaline_Phosphotase,
                record.Alamine_Aminotransferase,
                record.Aspartate_Aminotransferase,
                record.Total_Proteins,
                record.Albumin,
                record.Albumin_and_Globulin_Ratio
            ]
            
            input_data = np.array(features).reshape(1, -1)
            prediction = model.predict(input_data)[0]
            # INVERT prediction
            prediction = 1 - prediction
            probability = model.predict_proba(input_data)[0] if hasattr(model, 'predict_proba') else None
            # Invert probability order if exists
            if probability is not None:
                probability = probability[::-1]
            
            result = {
                'index': idx,
                'prediction': int(prediction),
                'status': 'Liver Disease Detected' if prediction == 1 else 'No Liver Disease',
            }
            
            if probability is not None:
                result['confidence'] = float(max(probability)) * 100
            
            results.append(result)
        
        return {
            'total_records': len(results),
            'results': results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
