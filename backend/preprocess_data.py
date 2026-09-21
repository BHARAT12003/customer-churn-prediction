import pandas as pd
from pathlib import Path

# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "customer_churn.csv"
PROCESSED_PATH = BASE_DIR / "dataset" / "processed_churn.csv"


# ============================================================
# 2. LOAD DATASET
# ============================================================

print("\n" + "=" * 60)
print("       CUSTOMER CHURN DATA PREPROCESSING")
print("=" * 60)

df = pd.read_csv(DATASET_PATH)

print("\nOriginal dataset shape:")
print(df.shape)


# ============================================================
# 3. REMOVE CUSTOMER ID
# ============================================================

print("\n[1] Removing customerID...")

df = df.drop("customerID", axis=1)

print("customerID removed.")


# ============================================================
# 4. CONVERT TOTALCHARGES TO NUMERIC
# ============================================================

print("\n[2] Converting TotalCharges to numeric...")

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print("TotalCharges converted successfully.")


# ============================================================
# 5. CHECK MISSING VALUES
# ============================================================

print("\n[3] Checking missing values...")

missing_before = df.isnull().sum()

print("\nMissing values before cleaning:")

print(missing_before[missing_before > 0])


# ============================================================
# 6. HANDLE MISSING VALUES
# ============================================================

print("\n[4] Handling missing values...")

# TotalCharges contains blank values for some customers.
# Replace missing TotalCharges with the median value.

df["TotalCharges"] = df["TotalCharges"].fillna(
    df["TotalCharges"].median()
)

print("Missing values handled.")


# ============================================================
# 7. CONVERT TARGET VARIABLE
# ============================================================

print("\n[5] Converting Churn target...")

df["Churn"] = df["Churn"].map({
    "Yes": 1,
    "No": 0
})

print("Churn converted:")
print("No  → 0")
print("Yes → 1")


# ============================================================
# 8. ONE-HOT ENCODING
# ============================================================

print("\n[6] Encoding categorical variables...")

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

print("\nCategorical columns:")
print(list(categorical_columns))

df = pd.get_dummies(
    df,
    columns=categorical_columns,
    drop_first=True,
    dtype=int
)

print("\nCategorical variables encoded.")


# ============================================================
# 9. FINAL MISSING VALUE CHECK
# ============================================================

print("\n[7] Final missing-value check...")

total_missing = df.isnull().sum().sum()

print(f"Total missing values: {total_missing}")


# ============================================================
# 10. SAVE PROCESSED DATASET
# ============================================================

df.to_csv(PROCESSED_PATH, index=False)

print("\n[8] Processed dataset saved.")

print(f"Location:")
print(PROCESSED_PATH)


# ============================================================
# 11. FINAL DATASET INFORMATION
# ============================================================

print("\nFinal dataset shape:")
print(df.shape)

print("\nFirst 5 processed records:")
print(df.head().to_string())

print("\n" + "=" * 60)
print("       PREPROCESSING COMPLETED")
print("=" * 60)