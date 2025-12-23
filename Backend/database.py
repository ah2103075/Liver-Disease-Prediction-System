import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), 'liver_disease.db')

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Prediction history table
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        age REAL NOT NULL,
        gender TEXT NOT NULL,
        tb REAL NOT NULL,
        db REAL NOT NULL,
        alkphos REAL NOT NULL,
        sgpt REAL NOT NULL,
        sgot REAL NOT NULL,
        tp REAL NOT NULL,
        alb REAL NOT NULL,
        ag_ratio REAL NOT NULL,
        prediction INTEGER NOT NULL,
        status TEXT NOT NULL,
        confidence REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

# User functions
def add_user(username: str, password: str, email: str, full_name: str) -> bool:
    """Add a new user to the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO users (username, password, email, full_name)
                     VALUES (?, ?, ?, ?)''', 
                  (username, password, email, full_name))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username: str) -> Optional[Dict]:
    """Get user by username"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, username, password, email, full_name, created_at FROM users WHERE username = ?', 
              (username,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'email': row[3],
            'full_name': row[4],
            'created_at': row[5]
        }
    return None

def user_exists(username: str) -> bool:
    """Check if user exists"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

# Prediction history functions
def add_prediction(user_id: int, age: float, gender: str, tb: float, db: float,
                   alkphos: float, sgpt: float, sgot: float, tp: float, alb: float,
                   ag_ratio: float, prediction: int, status: str, confidence: float) -> bool:
    """Add a prediction to history"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO predictions 
                     (user_id, age, gender, tb, db, alkphos, sgpt, sgot, tp, alb, ag_ratio, prediction, status, confidence)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (user_id, age, gender, tb, db, alkphos, sgpt, sgot, tp, alb, ag_ratio, prediction, status, confidence))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding prediction: {e}")
        return False

def get_user_predictions(user_id: int) -> List[Dict]:
    """Get all predictions for a user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT id, user_id, age, gender, tb, db, tp, alb, ag_ratio, sgpt, sgot, alkphos, 
                 prediction, status, confidence, created_at 
                 FROM predictions WHERE user_id = ? ORDER BY created_at DESC''',
              (user_id,))
    rows = c.fetchall()
    conn.close()
    
    import json
    predictions = []
    for row in rows:
        medical_params = {
            'Age': row[2],
            'Gender': 1 if row[3] == 'Male' else 0,
            'Total_Bilirubin': row[4],
            'Direct_Bilirubin': row[5],
            'Total_Proteins': row[6],
            'Albumin': row[7],
            'Albumin_and_Globulin_Ratio': row[8],
            'Alamine_Aminotransferase': row[9],
            'Aspartate_Aminotransferase': row[10],
            'Alkaline_Phosphotase': row[11]
        }
        predictions.append({
            'id': row[0],
            'medical_parameters': json.dumps(medical_params),
            'prediction': row[12],
            'status': row[13],
            'confidence': row[14],
            'timestamp': row[15]
        })
    return predictions

def delete_prediction(prediction_id: int, user_id: int) -> bool:
    """Delete a specific prediction"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM predictions WHERE id = ? AND user_id = ?', 
                  (prediction_id, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting prediction: {e}")
        return False

def clear_user_history(user_id: int) -> bool:
    """Clear all predictions for a user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM predictions WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing history: {e}")
        return False
