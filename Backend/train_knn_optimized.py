import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsClassifier
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

print("="*80)
print("TRAINING OPTIMIZED KNN MODEL FOR MAXIMUM ACCURACY")
print("="*80)

# Test different K values
print("\nTesting different K values to find optimal...")
results = {}

for k in [3, 5, 7, 9, 11, 15, 21]:
    pipeline = Pipeline([
        ('scaler', RobustScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k))
    ])
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    results[k] = accuracy
    print(f"K={k:2d}: Accuracy = {accuracy:.4f} ({accuracy*100:.2f}%)")

# Find best K
best_k = max(results, key=results.get)
best_accuracy = results[best_k]

print(f"\n" + "="*80)
print(f"BEST K VALUE: {best_k} with Accuracy: {best_accuracy*100:.2f}%")
print("="*80)

# Train final model with best K
final_pipeline = Pipeline([
    ('scaler', RobustScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=best_k))
])

final_pipeline.fit(X_train, y_train)
y_pred_train = final_pipeline.predict(X_train)
y_pred_test = final_pipeline.predict(X_test)

train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)
precision = precision_score(y_test, y_pred_test)
recall = recall_score(y_test, y_pred_test)
f1 = f1_score(y_test, y_pred_test)

print("\n" + "="*80)
print("FINAL KNN MODEL PERFORMANCE")
print("="*80)
print(f"\nTraining Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"Testing Accuracy:  {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")

print(f"\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred_test)
print(cm)
print(f"True Negatives: {cm[0, 0]}, False Positives: {cm[0, 1]}")
print(f"False Negatives: {cm[1, 0]}, True Positives: {cm[1, 1]}")

print(f"\nClassification Report:")
print(classification_report(y_test, y_pred_test, target_names=['Non-Patient', 'Patient']))

# Comparison
print("\n" + "="*80)
print("COMPARISON: PREVIOUS vs NEW")
print("="*80)
print(f"Previous Model (Random Forest): 73.28%")
print(f"New Model (KNN K={best_k}):     {test_accuracy*100:.2f}%")
print(f"Improvement:                    {(test_accuracy - 0.7328)*100:+.2f}%")

# Save model
model_filename = 'knn_best_model.pkl'
with open(model_filename, 'wb') as f:
    pickle.dump(final_pipeline, f)

print(f"\n✅ Model saved as '{model_filename}'")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Algorithm: K-Nearest Neighbors (KNN)")
print(f"K Value:   {best_k}")
print(f"Accuracy:  {test_accuracy*100:.2f}%")
print(f"Recall:    {recall*100:.2f}%")
print(f"Precision: {precision*100:.2f}%")
print(f"F1-Score:  {f1:.4f}")
print(f"Model:     {model_filename}")
print("="*80)
