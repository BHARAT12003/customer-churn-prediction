import pandas as pd
from pathlib import Path

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATASET_PATH = BASE_DIR / "dataset" / "customer_churn.csv"

# Load dataset
df = pd.read_csv(DATASET_PATH)

print("\n" + "=" * 60)
print("       CUSTOMER CHURN DATASET ANALYSIS")
print("=" * 60)

# 1. Dataset shape
print("\n1. DATASET SIZE")
print("-" * 40)
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# 2. Column names
print("\n2. COLUMN NAMES")
print("-" * 40)

for i, column in enumerate(df.columns, start=1):
    print(f"{i:2}. {column}")

# 3. First five records
print("\n3. FIRST 5 RECORDS")
print("-" * 40)
print(df.head().to_string())

# 4. Data types
print("\n4. DATA TYPES")
print("-" * 40)
print(df.dtypes)

# 5. Missing values
print("\n5. MISSING VALUES")
print("-" * 40)

missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])

# 6. Duplicate records
print("\n6. DUPLICATE RECORDS")
print("-" * 40)
print(f"Duplicate rows: {df.duplicated().sum()}")

# 7. Churn distribution
print("\n7. CHURN DISTRIBUTION")
print("-" * 40)
print(df["Churn"].value_counts())

# 8. Churn percentage
print("\n8. CHURN PERCENTAGE")
print("-" * 40)

churn_percentage = df["Churn"].value_counts(normalize=True) * 100

for category, percentage in churn_percentage.items():
    print(f"{category}: {percentage:.2f}%")

# 9. Numerical summary
print("\n9. NUMERICAL DATA SUMMARY")
print("-" * 40)
print(df.describe().to_string())

print("\n" + "=" * 60)
print("       DATASET ANALYSIS COMPLETED")
print("=" * 60)