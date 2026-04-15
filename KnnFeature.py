'''To reduce the dataset to top n features using feature importance from a model, Random Forest is the most suitable choice because:

1. It provides built-in feature importance scores
2. Handles high-dimensional data well (Breast Cancer dataset has 30 features)
3. Robust to outliers and scaling

Here's the modified code that uses Random Forest to select top n features:

'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, stratify=cancer.target, random_state=66
)

# Train Random Forest to get feature importance
rf = RandomForestClassifier(n_estimators=100, random_state=66)
rf.fit(X_train, y_train)

# Get feature importance scores
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]

# Select top n features (let's say top 10)
n_features = 10
selector = SelectFromModel(rf, max_features=n_features, threshold=-np.inf)
selector.fit(X_train, y_train)

# Transform the data to keep only top n features
X_train_selected = selector.transform(X_train)
X_test_selected = selector.transform(X_test)

print(f"Original number of features: {X_train.shape[1]}")
print(f"Reduced number of features: {X_train_selected.shape[1]}")

# Display top features
print(f"\nTop {n_features} features:")
for i in range(n_features):
    print(f"{i+1}. {cancer.feature_names[indices[i]]}: {importances[indices[i]]:.4f}")

# Train KNN on reduced features
training_accuracy = []
test_accuracy = []
neighbors_settings = range(1, 11)

for n_neighbors in neighbors_settings:
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train_selected, y_train)
    training_accuracy.append(clf.score(X_train_selected, y_train))
    test_accuracy.append(clf.score(X_test_selected, y_test))

# Plot results
plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
plt.legend()
plt.title(f"KNN Performance with Top {n_features} Features (Random Forest Selection)")
plt.show()
```

Alternative: Using SVM with Recursive Feature Elimination (RFE)

If you prefer SVM for feature selection:

```python
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.feature_selection import RFE

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, stratify=cancer.target, random_state=66
)

# Use SVM with RFE for feature selection
svm = SVC(kernel='linear', random_state=66)
n_features = 10
selector = RFE(svm, n_features_to_select=n_features)
selector.fit(X_train, y_train)

X_train_selected = selector.transform(X_train)
X_test_selected = selector.transform(X_test)

print(f"Original features: {X_train.shape[1]} → Reduced to: {X_train_selected.shape[1]}")

# Train KNN on reduced features
training_accuracy = []
test_accuracy = []
neighbors_settings = range(1, 11)

for n_neighbors in neighbors_settings:
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train_selected, y_train)
    training_accuracy.append(clf.score(X_train_selected, y_train))
    test_accuracy.append(clf.score(X_test_selected, y_test))

plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
plt.legend()
plt.title(f"KNN with Top {n_features} Features (SVM-RFE Selection)")
plt.show()
```

Why Random Forest is best for this task:

· ✅ Handles feature interactions naturally
· ✅ Provides reliable feature importance scores
· ✅ Works well without scaling (unlike SVM)
· ✅ Fast computation on 30 features

You can adjust n_features to experiment with different numbers of features.
