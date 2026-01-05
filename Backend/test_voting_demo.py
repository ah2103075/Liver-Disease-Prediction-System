"""
Test script to demonstrate the voting ensemble system
Shows examples of majority voting logic
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import warnings
warnings.filterwarnings('ignore')

def test_voting_system():
    """Test the voting ensemble with sample predictions"""
    
    print("\n" + "="*80)
    print("VOTING ENSEMBLE SYSTEM - TEST DEMONSTRATION")
    print("="*80)
    
    # Load the trained ensemble model
    ensemble_model_path = 'voting_ensemble_model.pkl'
    
    if not os.path.exists(ensemble_model_path):
        print("ERROR: voting_ensemble_model.pkl not found!")
        print("Please run 'train_voting_ensemble.py' first.")
        return
    
    with open(ensemble_model_path, 'rb') as f:
        ensemble_data = pickle.load(f)
        knn_model = ensemble_data['knn_pipeline']
        rf_model = ensemble_data['rf_pipeline']
        svm_model = ensemble_data['svm_pipeline']
    
    # Load the dataset for testing
    csv_path = 'Indian Liver Patient Dataset (ILPD).csv'
    df = pd.read_csv(csv_path)
    
    # Convert Gender to numeric if it's string
    if df['Gender'].dtype == 'object':
        df['Gender'] = (df['Gender'] == 'Male').astype(int)
    
    # Handle missing values
    df = df.dropna()
    
    X = df.drop('is_patient', axis=1)
    y = df['is_patient']
    
    # Split data
    _, test_data, _, test_labels = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    print("\n[SUCCESS] Models loaded successfully!")
    print("Total test samples: {}".format(len(test_data)))
    
    # Test voting logic with specific examples
    print("\n" + "="*80)
    print("VOTING LOGIC EXAMPLES")
    print("="*80)
    
    test_cases = [
        {
            'name': 'Case 1: KNN=Yes, RF=Yes, SVM=No',
            'knn': 1,
            'rf': 1,
            'svm': 0,
            'expected': 'Yes (2/3 voted Yes)'
        },
        {
            'name': 'Case 2: KNN=No, RF=No, SVM=Yes',
            'knn': 0,
            'rf': 0,
            'svm': 1,
            'expected': 'No (2/3 voted No)'
        },
        {
            'name': 'Case 3: KNN=Yes, RF=Yes, SVM=Yes',
            'knn': 1,
            'rf': 1,
            'svm': 1,
            'expected': 'Yes (3/3 voted Yes - Unanimous)'
        },
        {
            'name': 'Case 4: KNN=No, RF=No, SVM=No',
            'knn': 0,
            'rf': 0,
            'svm': 0,
            'expected': 'No (3/3 voted No - Unanimous)'
        },
        {
            'name': 'Case 5: KNN=Yes, RF=No, SVM=No',
            'knn': 1,
            'rf': 0,
            'svm': 0,
            'expected': 'No (1/3 voted Yes)'
        }
    ]
    
    for case in test_cases:
        votes = [case['knn'], case['rf'], case['svm']]
        result = 1 if sum(votes) >= 2 else 0
        agreement = sum([case['knn'] == result, case['rf'] == result, case['svm'] == result])
        confidence = (agreement / 3) * 100
        
        print("\n{}".format(case['name']))
        print("  KNN: {} | RF: {} | SVM: {}".format(
            'Yes' if case['knn'] == 1 else 'No',
            'Yes' if case['rf'] == 1 else 'No',
            'Yes' if case['svm'] == 1 else 'No'
        ))
        print("  -> Voting Result: {} (Disease Detected)".format(
            'YES' if result == 1 else 'NO (No Disease)'
        ))
        print("  -> Confidence: {:.2f}% ({}/3 models agree)".format(confidence, agreement))
        print("  -> Expected: {}".format(case['expected']))
    
    # Real predictions from test set
    print("\n" + "="*80)
    print("REAL PREDICTIONS FROM TEST SET (First 15 samples)")
    print("="*80)
    
    sample_size = min(15, len(test_data))
    sample_indices = np.arange(sample_size)
    
    print("\n{:<8} {:<6} {:<6} {:<6} {:<6} {:<10} {:<12} {:<20}".format(
        'Index', 'True', 'KNN', 'RF', 'SVM', 'Ensemble', 'Confidence', 'Status'
    ))
    print("-" * 90)
    
    correct = 0
    for i, idx in enumerate(sample_indices):
        X = test_data.iloc[idx:idx+1].values
        y_true = test_labels.iloc[idx]
        
        knn_pred = knn_model.predict(X)[0]
        rf_pred = rf_model.predict(X)[0]
        svm_pred = svm_model.predict(X)[0]
        
        votes = [knn_pred, rf_pred, svm_pred]
        ensemble_pred = 1 if sum(votes) >= 2 else 0
        agreement_count = sum([knn_pred == ensemble_pred, rf_pred == ensemble_pred, svm_pred == ensemble_pred])
        confidence = (agreement_count / 3) * 100
        
        is_correct = "CORRECT" if ensemble_pred == y_true else "WRONG"
        if ensemble_pred == y_true:
            correct += 1
        
        print("{:<8} {:<6} {:<6} {:<6} {:<6} {:<10} {:<12.2f}% {:<20}".format(
            idx, int(y_true), int(knn_pred), int(rf_pred), int(svm_pred), 
            int(ensemble_pred), confidence, is_correct
        ))
    
    accuracy = (correct / sample_size) * 100
    print("\nAccuracy on sample: {}/{} = {:.2f}%".format(correct, sample_size, accuracy))
    
    # Detailed voting breakdown
    print("\n" + "="*80)
    print("VOTING BREAKDOWN ON FULL TEST SET")
    print("="*80)
    
    all_knn_preds = knn_model.predict(test_data.values)
    all_rf_preds = rf_model.predict(test_data.values)
    all_svm_preds = svm_model.predict(test_data.values)
    
    unanimous_yes = 0
    unanimous_no = 0
    two_votes_yes = 0
    two_votes_no = 0
    
    for i in range(len(test_data)):
        votes = [all_knn_preds[i], all_rf_preds[i], all_svm_preds[i]]
        vote_sum = sum(votes)
        
        if vote_sum == 3:
            unanimous_yes += 1
        elif vote_sum == 0:
            unanimous_no += 1
        elif vote_sum == 2:
            two_votes_yes += 1
        else:  # vote_sum == 1
            two_votes_no += 1
    
    print("\nUnanimous 'Yes' (3/3): {} cases".format(unanimous_yes))
    print("Unanimous 'No'  (0/3): {} cases".format(unanimous_no))
    print("Majority 'Yes'  (2/3): {} cases".format(two_votes_yes))
    print("Majority 'No'   (1/3): {} cases".format(two_votes_no))
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("""
The voting ensemble uses MAJORITY VOTING:
- If >=2 out of 3 algorithms predict 'Yes' -> Result is 'Yes' (Disease Detected)
- If <=1 out of 3 algorithms predict 'Yes' -> Result is 'No' (No Disease)

Benefits:
* More robust predictions than single algorithm
* Reduces overfitting by combining different models
* Better generalization to new data
* Confidence based on algorithm agreement

Models Used:
1. K-Nearest Neighbors (KNN) - Instance-based learning
2. Random Forest (RF) - Ensemble of decision trees
3. Support Vector Machine (SVM) - Margin-based classifier
""")

if __name__ == "__main__":
    test_voting_system()
