import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import pickle
import warnings
warnings.filterwarnings('ignore')

# 1. LOAD DATASET
df = pd.read_csv('Indian Liver Patient Dataset (ILPD).csv')

df.columns = ['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase', 
              'Alamine_Aminotransferase', 'Aspartate_Aminotransferase', 'Total_Proteins', 'Albumin', 
              'Albumin_and_Globulin_Ratio', 'is_patient']

# Convert Gender
df['Gender'] = df['Gender'].apply(lambda x: 1 if x.upper() in ['M', 'MALE'] else 0)

# Remove NaN
df = df.dropna()

# Handle outliers
numeric_cols = ['Age', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase', 
                'Alamine_Aminotransferase', 'Aspartate_Aminotransferase', 'Total_Proteins', 
                'Albumin', 'Albumin_and_Globulin_Ratio']

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[col] = df[col].clip(lower_bound, upper_bound)

df['is_patient'] = (df['is_patient'] == 1).astype(int)

X = df[['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase', 
        'Alamine_Aminotransferase', 'Aspartate_Aminotransferase', 'Total_Proteins', 'Albumin', 
        'Albumin_and_Globulin_Ratio']]
y = df['is_patient']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("="*100)
print("TRAINING VOTING ENSEMBLE: KNN + RANDOM FOREST + SVM")
print("="*100)

# ==================== TRAIN KNN ====================
print("\n" + "="*100)
print("1. TRAINING K-NEAREST NEIGHBORS (KNN)")
print("="*100)

results_knn = {}
for k in [3, 5, 7, 9, 11]:
    pipeline = Pipeline([
        ('scaler', RobustScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k))
    ])
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    results_knn[k] = accuracy
    print(f"K={k:2d}: Accuracy = {accuracy*100:.2f}%")

best_k = max(results_knn, key=results_knn.get)

knn_pipeline = Pipeline([
    ('scaler', RobustScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=best_k))
])
knn_pipeline.fit(X_train, y_train)
y_pred_knn = knn_pipeline.predict(X_test)
knn_accuracy = accuracy_score(y_test, y_pred_knn)

print(f"\n✅ Best KNN K={best_k}, Accuracy: {knn_accuracy*100:.2f}%")

# ==================== TRAIN RANDOM FOREST ====================
print("\n" + "="*100)
print("2. TRAINING RANDOM FOREST")
print("="*100)

rf_params = [
    {'n_estimators': 50, 'max_depth': 10},
    {'n_estimators': 100, 'max_depth': 15},
    {'n_estimators': 200, 'max_depth': 20},
]

results_rf = {}
for i, params in enumerate(rf_params):
    pipeline = Pipeline([
        ('scaler', RobustScaler()),
        ('rf', RandomForestClassifier(random_state=42, n_jobs=-1, **params))
    ])
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    results_rf[i] = (accuracy, params)
    print(f"Config {i+1} (n_estimators={params['n_estimators']}, max_depth={params['max_depth']}): Accuracy = {accuracy*100:.2f}%")

best_rf_idx = max(results_rf, key=lambda x: results_rf[x][0])
best_rf_params = results_rf[best_rf_idx][1]

rf_pipeline = Pipeline([
    ('scaler', RobustScaler()),
    ('rf', RandomForestClassifier(random_state=42, n_jobs=-1, **best_rf_params))
])
rf_pipeline.fit(X_train, y_train)
y_pred_rf = rf_pipeline.predict(X_test)
rf_accuracy = accuracy_score(y_test, y_pred_rf)

print(f"\n✅ Best Random Forest: n_estimators={best_rf_params['n_estimators']}, max_depth={best_rf_params['max_depth']}, Accuracy: {rf_accuracy*100:.2f}%")

# ==================== TRAIN SVM ====================
print("\n" + "="*100)
print("3. TRAINING SUPPORT VECTOR MACHINE (SVM)")
print("="*100)

svm_params = [
    {'kernel': 'rbf', 'C': 0.1},
    {'kernel': 'rbf', 'C': 1},
    {'kernel': 'rbf', 'C': 10},
    {'kernel': 'linear', 'C': 1},
]

results_svm = {}
for i, params in enumerate(svm_params):
    pipeline = Pipeline([
        ('scaler', RobustScaler()),
        ('svm', SVC(random_state=42, **params))
    ])
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    results_svm[i] = (accuracy, params)
    print(f"Config {i+1} (kernel='{params['kernel']}', C={params['C']}): Accuracy = {accuracy*100:.2f}%")

best_svm_idx = max(results_svm, key=lambda x: results_svm[x][0])
best_svm_params = results_svm[best_svm_idx][1]

svm_pipeline = Pipeline([
    ('scaler', RobustScaler()),
    ('svm', SVC(random_state=42, probability=True, **best_svm_params))
])
svm_pipeline.fit(X_train, y_train)
y_pred_svm = svm_pipeline.predict(X_test)
svm_accuracy = accuracy_score(y_test, y_pred_svm)

print(f"\n✅ Best SVM: kernel='{best_svm_params['kernel']}', C={best_svm_params['C']}, Accuracy: {svm_accuracy*100:.2f}%")

# ==================== VOTING ENSEMBLE ====================
print("\n" + "="*100)
print("4. VOTING ENSEMBLE (MAJORITY VOTING: 2 out of 3)")
print("="*100)

# Combine predictions using majority voting (2 out of 3 must agree)
ensemble_predictions = []
for i in range(len(y_pred_knn)):
    votes = [y_pred_knn[i], y_pred_rf[i], y_pred_svm[i]]
    # Majority voting: if at least 2 algorithms predict 1, result is 1, otherwise 0
    prediction = 1 if sum(votes) >= 2 else 0
    ensemble_predictions.append(prediction)

ensemble_predictions = np.array(ensemble_predictions)
ensemble_accuracy = accuracy_score(y_test, ensemble_predictions)
ensemble_precision = precision_score(y_test, ensemble_predictions)
ensemble_recall = recall_score(y_test, ensemble_predictions)
ensemble_f1 = f1_score(y_test, ensemble_predictions)

print(f"\n✅ Ensemble (Voting System) Accuracy: {ensemble_accuracy*100:.2f}%")
print(f"   Precision: {ensemble_precision*100:.2f}%")
print(f"   Recall:    {ensemble_recall*100:.2f}%")
print(f"   F1-Score:  {ensemble_f1:.4f}")

# ==================== COMPARISON ====================
print("\n" + "="*100)
print("ALGORITHM COMPARISON")
print("="*100)
print(f"KNN (K={best_k})           : {knn_accuracy*100:.2f}%")
print(f"Random Forest (n={best_rf_params['n_estimators']}): {rf_accuracy*100:.2f}%")
print(f"SVM ({best_svm_params['kernel']}, C={best_svm_params['C']})        : {svm_accuracy*100:.2f}%")
print(f"{'─'*50}")
print(f"Voting Ensemble (2/3)     : {ensemble_accuracy*100:.2f}%")

# ==================== DETAILED METRICS ====================
print("\n" + "="*100)
print("DETAILED ENSEMBLE METRICS")
print("="*100)

cm_ensemble = confusion_matrix(y_test, ensemble_predictions)
print(f"\nConfusion Matrix:")
print(cm_ensemble)
print(f"True Negatives: {cm_ensemble[0, 0]}, False Positives: {cm_ensemble[0, 1]}")
print(f"False Negatives: {cm_ensemble[1, 0]}, True Positives: {cm_ensemble[1, 1]}")

print(f"\nClassification Report:")
print(classification_report(y_test, ensemble_predictions, target_names=['Non-Patient', 'Patient']))

# ==================== SAMPLE PREDICTIONS ====================
print("\n" + "="*100)
print("SAMPLE PREDICTIONS (First 10 Test Cases)")
print("="*100)
print(f"{'Index':<6} {'True':<6} {'KNN':<6} {'RF':<6} {'SVM':<6} {'Ensemble':<10} {'Result'}")
print(f"{'-'*60}")

for i in range(min(10, len(y_test))):
    true_label = y_test.iloc[i]
    knn_pred = y_pred_knn[i]
    rf_pred = y_pred_rf[i]
    svm_pred = y_pred_svm[i]
    ensemble_pred = ensemble_predictions[i]
    result = "✓ CORRECT" if ensemble_pred == true_label else "✗ WRONG"
    
    print(f"{i:<6} {true_label:<6} {knn_pred:<6} {rf_pred:<6} {svm_pred:<6} {ensemble_pred:<10} {result}")

# ==================== SAVE MODELS ====================
print("\n" + "="*100)
print("SAVING MODELS")
print("="*100)

# Save individual models
model_data = {
    'knn_pipeline': knn_pipeline,
    'rf_pipeline': rf_pipeline,
    'svm_pipeline': svm_pipeline,
    'knn_accuracy': knn_accuracy,
    'rf_accuracy': rf_accuracy,
    'svm_accuracy': svm_accuracy,
    'ensemble_accuracy': ensemble_accuracy,
    'ensemble_precision': ensemble_precision,
    'ensemble_recall': ensemble_recall,
    'ensemble_f1': ensemble_f1,
}

with open('voting_ensemble_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print(f"✅ Voting Ensemble Model saved as 'voting_ensemble_model.pkl'")

# Save individual models for reference
with open('knn_model.pkl', 'wb') as f:
    pickle.dump(knn_pipeline, f)
print(f"✅ KNN Model saved as 'knn_model.pkl'")

with open('rf_model.pkl', 'wb') as f:
    pickle.dump(rf_pipeline, f)
print(f"✅ Random Forest Model saved as 'rf_model.pkl'")

with open('svm_model.pkl', 'wb') as f:
    pickle.dump(svm_pipeline, f)
print(f"✅ SVM Model saved as 'svm_model.pkl'")

# ==================== FINAL SUMMARY ====================
print("\n" + "="*100)
print("SUMMARY")
print("="*100)
print(f"Voting Ensemble Accuracy: {ensemble_accuracy*100:.2f}%")
print(f"Precision: {ensemble_precision*100:.2f}%")
print(f"Recall:    {ensemble_recall*100:.2f}%")
print(f"F1-Score:  {ensemble_f1:.4f}")
print(f"\nVoting Strategy: Majority Voting (2 out of 3 algorithms must agree)")
print(f"  - If ≥2 algorithms predict 'Yes' → Result is 'Yes'")
print(f"  - If ≤1 algorithms predict 'Yes' → Result is 'No'")
print("="*100)
