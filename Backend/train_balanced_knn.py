import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from imblearn.over_sampling import SMOTE
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("TRAINING KNN MODEL WITH BALANCED DATA (SMOTE)")
print("=" * 70)

# Load dataset
print("\n1️⃣  Loading dataset...")
df = pd.read_csv('Indian Liver Patient Dataset (ILPD).csv')

# Remove rows with NaN values
df = df.dropna()
print(f"   Total samples: {len(df)}")

# Convert Gender: 'Male'/'Female' to 1/0 if needed
if df.iloc[:, 1].dtype == 'object':
    df.iloc[:, 1] = df.iloc[:, 1].map({'Male': 1, 'Female': 0, 1: 1, 0: 0})

# Convert all columns to numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna()

# Separate features and target
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# Convert labels: 1=patient, 2=non-patient → 1=patient, 0=non-patient
y = np.where(y == 1, 1, 0)

print(f"   Class distribution (original):")
print(f"   - Disease (1): {np.sum(y == 1)} samples")
print(f"   - Healthy (0): {np.sum(y == 0)} samples")

# Split data
print("\n2️⃣  Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Training set: {len(X_train)} samples")
print(f"   Test set: {len(X_test)} samples")

# Apply SMOTE to balance training data
print("\n3️⃣  Applying SMOTE to balance training data...")
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

print(f"   Balanced training samples: {len(X_train_balanced)}")
print(f"   Class distribution (balanced):")
print(f"   - Disease (1): {np.sum(y_train_balanced == 1)} samples")
print(f"   - Healthy (0): {np.sum(y_train_balanced == 0)} samples")

# Create pipeline with StandardScaler and KNN
print("\n4️⃣  Training KNN model with K=9...")
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', KNeighborsClassifier(n_neighbors=9))
])

pipeline.fit(X_train_balanced, y_train_balanced)
print("   ✅ Model trained successfully!")

# Make predictions
print("\n5️⃣  Evaluating model...")
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"   Test Accuracy: {accuracy * 100:.2f}%")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\n   Confusion Matrix:")
print(f"   True Negatives (TN):  {cm[0, 0]}")
print(f"   False Positives (FP): {cm[0, 1]}")
print(f"   False Negatives (FN): {cm[1, 0]}")
print(f"   True Positives (TP):  {cm[1, 1]}")

# Classification Report
print(f"\n   Classification Report:")
print(classification_report(y_test, y_pred, 
                          target_names=['Healthy (0)', 'Disease (1)']))

# Save model
print("\n6️⃣  Saving model...")
model_path = 'knn_model_balanced.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)
print(f"   ✅ Model saved as: {model_path}")

# Test with healthy data
print("\n7️⃣  Testing with healthy patient data...")
healthy_data = np.array([[28, 1, 0.4, 0.1, 50, 12, 18, 7.0, 4.3, 1.3]])
pred_healthy = pipeline.predict(healthy_data)[0]
conf_healthy = pipeline.predict_proba(healthy_data)[0]
print(f"   Healthy patient prediction: {pred_healthy}")
print(f"   Confidence: {max(conf_healthy) * 100:.2f}%")

# Test with disease data
print("\n8️⃣  Testing with disease patient data...")
disease_data = np.array([[55, 1, 1.5, 0.8, 120, 85, 95, 6.5, 3.0, 0.8]])
pred_disease = pipeline.predict(disease_data)[0]
conf_disease = pipeline.predict_proba(disease_data)[0]
print(f"   Disease patient prediction: {pred_disease}")
print(f"   Confidence: {max(conf_disease) * 100:.2f}%")

print("\n" + "=" * 70)
print("✅ TRAINING COMPLETE!")
print("=" * 70)
print(f"\n📊 Summary:")
print(f"   Model: knn_model_balanced.pkl")
print(f"   Algorithm: K-Nearest Neighbors (K=9)")
print(f"   Training: SMOTE-balanced data ({len(X_train_balanced)} samples)")
print(f"   Accuracy: {accuracy * 100:.2f}%")
print(f"\n🔄 To use this model:")
print(f"   1. Copy knn_model_balanced.pkl to update knn_model.pkl")
print(f"   2. Or modify main.py to load knn_model_balanced.pkl")
print(f"   3. Restart the backend server")
print("\n")
