
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# URL for the Wine dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data"

# Column names for the wine dataset
column_names = ['Class', 'Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash', 
                'Magnesium', 'Total phenols', 'Flavanoids', 'Nonflavanoid phenols',
                'Proanthocyanins', 'Color intensity', 'Hue', 
                'OD280/OD315 of diluted wines', 'Proline']

# Load the dataset
print("Loading Wine Dataset...")
df = pd.read_csv(url, names=column_names)

# Display dataset information
print(f"\nDataset shape: {df.shape}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nClass distribution:")
print(df['Class'].value_counts())
print(f"\nBasic statistics:")
print(df.describe())

# Separate features and target
X = df.drop('Class', axis=1)
y = df['Class']

# Split the data into training (70%) and testing (30%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"\nTraining set size: {X_train.shape[0]} samples")
print(f"Testing set size: {X_test.shape[0]} samples")
print(f"Number of features: {X_train.shape[1]}")

# Scale features for Logistic Regression (important for convergence)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Multinomial Logistic Regression model
print("\n" + "="*60)
print("Training Multinomial Logistic Regression Model")
print("="*60)

# Create Logistic Regression model with multinomial setting
mlr_model = LogisticRegression(
    multi_class='multinomial',  # Explicitly set multinomial
    solver='lbfgs',             # Good solver for multinomial
    max_iter=1000,              # Increased iterations for convergence
    random_state=42,
    C=1.0                       # Regularization strength
)

# Train the model
mlr_model.fit(X_train_scaled, y_train)

print("\nModel Training Complete!")
print(f"Number of iterations: {mlr_model.n_iter_[0]}")
print(f"Number of classes: {mlr_model.n_classes_}")
print(f"Classes: {mlr_model.classes_}")

# Make predictions
y_pred = mlr_model.predict(X_test_scaled)
y_pred_proba = mlr_model.predict_proba(X_test_scaled)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Display results
print("\n" + "="*60)
print("MULTINOMIAL LOGISTIC REGRESSION RESULTS")
print("="*60)

print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

print(f"\nConfusion Matrix:")
print(conf_matrix)

print(f"\nClassification Report:")
print(class_report)

# Detailed analysis
print("\n" + "="*60)
print("DETAILED ANALYSIS")
print("="*60)

# Per-class accuracy
per_class_accuracy = conf_matrix.diagonal() / conf_matrix.sum(axis=1)
for i, class_label in enumerate(mlr_model.classes_):
    print(f"\nClass {class_label} (Wine Type {class_label}):")
    print(f"  Accuracy: {per_class_accuracy[i]:.4f} ({per_class_accuracy[i]*100:.2f}%)")
    print(f"  Correct predictions: {conf_matrix[i,i]}")
    print(f"  Total samples: {conf_matrix.sum(axis=1)[i]}")

# Model coefficients (feature importance)
print("\n" + "="*60)
print("FEATURE COEFFICIENTS (Feature Importance)")
print("="*60)

coefficients = pd.DataFrame(
    mlr_model.coef_.T,
    columns=[f'Class_{c}' for c in mlr_model.classes_],
    index=X.columns
)

print("\nCoefficients for each class:")
print(coefficients)

# Top features for each class
print("\nTop 5 most important features for each wine type:")
for class_label in mlr_model.classes_:
    coef_col = f'Class_{class_label}'
    top_features = coefficients[coef_col].abs().sort_values(ascending=False).head(5)
    print(f"\nWine Type {class_label}:")
    for feature, coef in top_features.items():
        direction = "positive" if coefficients.loc[feature, coef_col] > 0 else "negative"
        print(f"  {feature}: {coefficients.loc[feature, coef_col]:.4f} ({direction} influence)")

# Prediction probabilities analysis
print("\n" + "="*60)
print("PREDICTION CONFIDENCE ANALYSIS")
print("="*60)

# Calculate average prediction confidence
avg_confidence = np.mean(np.max(y_pred_proba, axis=1))
print(f"\nAverage prediction confidence: {avg_confidence:.4f} ({avg_confidence*100:.2f}%)")

# Show some example predictions
print("\nSample predictions (first 10 test samples):")
print("-"*60)
for i in range(min(10, len(X_test))):
    true_class = y_test.iloc[i] if isinstance(y_test, pd.Series) else y_test[i]
    pred_class = y_pred[i]
    confidence = np.max(y_pred_proba[i])
    correct = "✓" if true_class == pred_class else "✗"
    print(f"Sample {i+1}: True={true_class}, Predicted={pred_class}, "
          f"Confidence={confidence:.3f}, {correct}")

# Cross-validation for robustness
print("\n" + "="*60)
print("CROSS-VALIDATION RESULTS")
print("="*60)

from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(mlr_model, X_train_scaled, y_train, cv=5, scoring='accuracy')
print(f"\n5-fold Cross-validation accuracy scores: {cv_scores}")
print(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# Compare with default parameters
print("\n" + "="*60)
print("PARAMETER COMPARISON")
print("="*60)

# Try different regularization strengths
C_values = [0.01, 0.1, 1, 10, 100]
cv_means = []

print("\nEffect of regularization strength (C) on accuracy:")
print(f"{'C value':<10} {'CV Accuracy':<15} {'Test Accuracy'}")
print("-"*40)

for C in C_values:
    mlr_temp = LogisticRegression(
        multi_class='multinomial',
        solver='lbfgs',
        max_iter=1000,
        random_state=42,
        C=C
    )
    cv_scores_temp = cross_val_score(mlr_temp, X_train_scaled, y_train, cv=5)
    mlr_temp.fit(X_train_scaled, y_train)
    test_acc = accuracy_score(y_test, mlr_temp.predict(X_test_scaled))
    print(f"{C:<10} {cv_scores_temp.mean():.4f}         {test_acc:.4f}")
    cv_means.append(cv_scores_temp.mean())

# Best C value
best_C = C_values[np.argmax(cv_means)]
print(f"\nBest C value based on CV: {best_C}")

# Train final model with best C
final_model = LogisticRegression(
    multi_class='multinomial',
    solver='lbfgs',
    max_iter=1000,
    random_state=42,
    C=best_C
)
final_model.fit(X_train_scaled, y_train)
final_accuracy = accuracy_score(y_test, final_model.predict(X_test_scaled))

print(f"\nFinal model accuracy with C={best_C}: {final_accuracy:.4f}")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

print(f"""
Dataset Information:
- Total samples: {len(df)}
- Features: {X.shape[1]}
- Classes: {len(df['Class'].unique())} (Wine types 1, 2, 3)
- Training samples: {X_train.shape[0]} (70%)
- Testing samples: {X_test.shape[0]} (30%)

Model Performance:
- Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)
- Cross-validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})
- Average Prediction Confidence: {avg_confidence:.4f}

Key Insights:
1. The model successfully distinguishes between all 3 wine types
2. Best performing class: Class {mlr_model.classes_[np.argmax(per_class_accuracy)]}
3. Features like Proline and Flavanoids have strong influence on predictions
4. Regularization strength (C={best_C}) optimizes the model
""")

# Optional: Visualize confusion matrix
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', 
                xticklabels=mlr_model.classes_, 
                yticklabels=mlr_model.classes_)
    plt.title('Confusion Matrix - Multinomial Logistic Regression')
    plt.xlabel('Predicted Class')
    plt.ylabel('Actual Class')
    plt.tight_layout()
    plt.show()
    
    # Feature importance visualization
    plt.figure(figsize=(10, 6))
    for class_label in mlr_model.classes_:
        coef_col = f'Class_{class_label}'
        plt.plot(coefficients[coef_col], marker='o', label=f'Wine Type {class_label}')
    
    plt.xlabel('Features')
    plt.ylabel('Coefficient Value')
    plt.title('Feature Coefficients for Each Wine Type')
    plt.legend()
    plt.xticks(range(len(X.columns)), X.columns, rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
except ImportError:
    print("\n(Matplotlib/seaborn not available for visualization)")

print("\n" + "="*60)
print("Model training complete!")
print("="*60)
