import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "processed_churn.csv"
MODEL_DIR = BASE_DIR / "model"

MODEL_DIR.mkdir(exist_ok=True)


# ============================================================
# LOAD DATASET
# ============================================================

print("\n" + "=" * 60)
print("              MODEL TRAINING")
print("=" * 60)

df = pd.read_csv(DATASET_PATH)

print("\nDataset loaded successfully.")
print("Dataset shape:", df.shape)


# ============================================================
# SEPARATE FEATURES AND TARGET
# ============================================================

X = df.drop("Churn", axis=1)
y = df["Churn"]

print("\nFeatures:", X.shape[1])
print("Target: Churn")


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples :", len(X_test))


# ============================================================
# FEATURE SCALING
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ============================================================
# DEFINE MODELS
# ============================================================

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=6,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}


# ============================================================
# TRAIN AND EVALUATE MODELS
# ============================================================

results = []

best_model = None
best_model_name = None
best_f1 = 0

print("\n" + "=" * 60)
print("              MODEL COMPARISON")
print("=" * 60)


for name, model in models.items():

    print(f"\nTraining {name}...")

    # Logistic Regression needs scaled data.
    # Tree-based models work directly with original features.
    if name == "Logistic Regression":
        model.fit(X_train_scaled, y_train)
        predictions = model.predict(X_test_scaled)
        probabilities = model.predict_proba(X_test_scaled)[:, 1]

    else:
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)
    roc_auc = roc_auc_score(y_test, probabilities)

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    })

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    # Select model using F1 score
    if f1 > best_f1:
        best_f1 = f1
        best_model = model
        best_model_name = name


# ============================================================
# DISPLAY COMPARISON TABLE
# ============================================================

results_df = pd.DataFrame(results)

print("\n" + "=" * 60)
print("              FINAL MODEL RESULTS")
print("=" * 60)

print(
    results_df.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision": "{:.4f}".format,
            "Recall": "{:.4f}".format,
            "F1 Score": "{:.4f}".format,
            "ROC-AUC": "{:.4f}".format
        }
    )
)


# ============================================================
# BEST MODEL
# ============================================================

print("\n" + "=" * 60)
print("              SELECTED MODEL")
print("=" * 60)

print(f"\nSelected model: {best_model_name}")
print(f"F1 Score: {best_f1:.4f}")


# ============================================================
# SAVE BEST MODEL
# ============================================================

model_path = MODEL_DIR / "churn_model.pkl"
scaler_path = MODEL_DIR / "scaler.pkl"
columns_path = MODEL_DIR / "feature_columns.pkl"

joblib.dump(best_model, model_path)
joblib.dump(scaler, scaler_path)
joblib.dump(list(X.columns), columns_path)


print("\nModel saved to:")
print(model_path)

print("\nScaler saved to:")
print(scaler_path)

print("\nFeature columns saved to:")
print(columns_path)


# ============================================================
# CONFUSION MATRIX
# ============================================================

if best_model_name == "Logistic Regression":
    best_predictions = best_model.predict(X_test_scaled)
else:
    best_predictions = best_model.predict(X_test)

cm = confusion_matrix(y_test, best_predictions)

print("\n" + "=" * 60)
print("              CONFUSION MATRIX")
print("=" * 60)

print(cm)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("          CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_test,
        best_predictions,
        target_names=["No Churn", "Churn"],
        zero_division=0
    )
)


print("\n" + "=" * 60)
print("        MODEL TRAINING COMPLETED")
print("=" * 60)