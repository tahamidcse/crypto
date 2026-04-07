import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# --- 1. Load Dataset ---
cols = ["fLength", "fWidth", "fSize", "fConc", "fConc1", "fAsym", "fM3Long", "fM3Trans", "fAlpha", "fDist", "class"]
df = pd.read_csv("magic04.data", names=cols)

# Convert class labels to integers: 'g' (gamma) becomes 1, others (hadron) become 0
df["class"] = (df["class"] == "g").astype(int)

# --- DEBUG: Check first few rows ---
print("=" * 50)
print("DATASET INFO")
print("=" * 50)
print(f"Dataset shape: {df.shape}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nClass distribution:")
print(df["class"].value_counts())
print(f"  - Gamma (1): {(df['class']==1).sum()}")
print(f"  - Hadron (0): {(df['class']==0).sum()}")
print(f"\nColumn names: {list(df.columns)}")
print("=" * 50)

# --- 2. Visualization (Optional) ---
# Uncomment if you want to see the plots
# for label in cols[:-1]:
#     plt.hist(df[df["class"]==1][label], color='blue', label='gamma', alpha=0.7, density=True)
#     plt.hist(df[df["class"]==0][label], color='red', label='hadron', alpha=0.7, density=True)
#     plt.title(label)
#     plt.ylabel("Probability")
#     plt.xlabel(label)
#     plt.legend()
#     plt.show()

# --- 3. Dataset Splitting ---
# Shuffle and split the data into Train (60%), Validation (20%), and Test (20%)
train, valid, test = np.split(df.sample(frac=1, random_state=42), [int(0.6*len(df)), int(0.8*len(df))])

print(f"\nSplit sizes:")
print(f"  Train: {len(train)} samples")
print(f"  Validation: {len(valid)} samples")
print(f"  Test: {len(test)} samples")

# --- 4. Preprocessing Function ---
def scale_dataset(dataframe, oversample=False):
    X = dataframe[dataframe.columns[:-1]].values
    y = dataframe[dataframe.columns[-1]].values
    
    print(f"    Before scaling - X shape: {X.shape}, y shape: {y.shape}")
    
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    if oversample:
        print(f"    Applying RandomOverSampler...")
        ros = RandomOverSampler(random_state=42)
        X, y = ros.fit_resample(X, y)
        print(f"    After oversampling - X shape: {X.shape}, y shape: {y.shape}")
    
    # Combine X and y back into one array
    data = np.hstack((X, np.reshape(y, (-1, 1))))
    
    return data, X, y

# Apply scaling and oversampling to the splits
print("\nProcessing training set (with oversampling):")
train, X_train, y_train = scale_dataset(train, oversample=True)

print("\nProcessing validation set (without oversampling):")
valid, X_valid, y_valid = scale_dataset(valid, oversample=False)

print("\nProcessing test set (without oversampling):")
test, X_test, y_test = scale_dataset(test, oversample=False)

# --- 5. K-Nearest Neighbors (KNN) with multiple k values ---
print("\n" + "=" * 50)
print("KNN MODEL EVALUATION")
print("=" * 50)

# Try different k values
k_values = [1, 3, 5, 7, 9, 11, 15, 21]
best_k = 5
best_accuracy = 0

for k in k_values:
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(X_train, y_train)
    
    # Predict on validation set
    y_valid_pred = knn_model.predict(X_valid)
    valid_accuracy = accuracy_score(y_valid, y_valid_pred)
    
    print(f"k={k:2d} -> Validation Accuracy: {valid_accuracy:.4f}")
    
    if valid_accuracy > best_accuracy:
        best_accuracy = valid_accuracy
        best_k = k

print(f"\n✅ Best k value: {best_k} with validation accuracy: {best_accuracy:.4f}")

# Train final model with best k
final_knn = KNeighborsClassifier(n_neighbors=best_k)
final_knn.fit(X_train, y_train)

# Evaluate on test set
y_pred = final_knn.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)

print(f"\n📊 Test Set Performance (k={best_k}):")
print(f"  Accuracy: {test_accuracy:.4f}")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Hadron (0)', 'Gamma (1)']))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:")
print(f"                 Predicted")
print(f"                 Hadron  Gamma")
print(f"  Actual Hadron  {cm[0,0]:6d}  {cm[0,1]:5d}")
print(f"         Gamma   {cm[1,0]:6d}  {cm[1,1]:5d}")

# Optional: Feature importance analysis (for KNN, we can check which features have highest variance)
print("\n" + "=" * 50)
print("FEATURE STATISTICS")
print("=" * 50)
feature_means = df.iloc[:, :-1].mean()
feature_stds = df.iloc[:, :-1].std()
feature_stats = pd.DataFrame({
    'Mean': feature_means,
    'Std Dev': feature_stds,
    'Variance': feature_stds**2
})
print(feature_stats.round(4))
