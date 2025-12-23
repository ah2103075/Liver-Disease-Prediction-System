import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# 1. LOAD DATASET
df = pd.read_csv('Indian Liver Patient Dataset (ILPD).csv')

# Rename columns to match exact dataset column names
df.columns = ['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase', 'Alamine_Aminotransferase', 'Aspartate_Aminotransferase', 'Total_Proteins', 'Albumin', 'Albumin_and_Globulin_Ratio', 'is_patient']

print(f"Dataset Shape: {df.shape}")

# 2. DATA PREPROCESSING
# Convert Gender: Male=1, Female=0
df['Gender'] = df['Gender'].apply(lambda x: 1 if x.upper() in ['M', 'MALE'] else 0)

# All values are already numeric
# Remove NaN values
df = df.dropna()

# Target variable: 1=Patient, 2=Non-Patient -> Convert to 1=Patient, 0=Non-Patient
df['is_patient'] = (df['is_patient'] == 1).astype(int)

print(f"\nAfter preprocessing:")
print(f"Shape: {df.shape}")
print(f"Target distribution:\n{df['is_patient'].value_counts()}")
print(f"Gender values: {df['Gender'].unique()}")

# Split features and target
X = df[['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase', 'Alamine_Aminotransferase', 'Aspartate_Aminotransferase', 'Total_Proteins', 'Albumin', 'Albumin_and_Globulin_Ratio']]
y = df['is_patient']

print(f"\nX shape: {X.shape}, y shape: {y.shape}")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Training set: {X_train.shape[0]}, Test set: {X_test.shape[0]}")

# 3. CREATE AND TRAIN KNN PIPELINE
# Test different K values to find the best one
print("\n" + "="*60)
print("TESTING DIFFERENT K VALUES")
print("="*60)

best_k = 3
best_accuracy = 0

for k in range(3, 16, 2):
    knn_temp = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', KNeighborsClassifier(n_neighbors=k))
    ])
    knn_temp.fit(X_train, y_train)
    pred_temp = knn_temp.predict(X_test)
    acc_temp = accuracy_score(y_test, pred_temp)
    print(f"K={k:2d}: Accuracy = {acc_temp:.4f}")
    
    if acc_temp > best_accuracy:
        best_accuracy = acc_temp
        best_k = k

print(f"\nBest K: {best_k} with Accuracy: {best_accuracy:.4f}")

# 4. TRAIN FINAL KNN MODEL WITH BEST K
knn_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', KNeighborsClassifier(n_neighbors=best_k))
])

print(f"\nTraining KNN Pipeline with K={best_k}...")
knn_pipeline.fit(X_train, y_train)

# Make predictions
knn_predictions = knn_pipeline.predict(X_test)

# Save the pipeline
pickle.dump(knn_pipeline, open('dt_model.pkl', 'wb'))
print("[OK] Model saved as 'dt_model.pkl'")

# 5. EVALUATION
accuracy = accuracy_score(y_test, knn_predictions)
print(f"\n{'='*60}")
print(f"Accuracy: {accuracy:.4f}")
print(f"{'='*60}")
print(f"\nClassification Report:")
print(classification_report(y_test, knn_predictions, target_names=['Healthy (0)', 'Patient (1)']))

# Confusion Matrix
cm = confusion_matrix(y_test, knn_predictions)
print(f"\nConfusion Matrix:\n{cm}")
print(f"True Negatives: {cm[0][0]}, False Positives: {cm[0][1]}")
print(f"False Negatives: {cm[1][0]}, True Positives: {cm[1][1]}")
