import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "customer_churn.csv"
RESULTS_DIR = BASE_DIR / "results"

# Create results directory if it doesn't exist
RESULTS_DIR.mkdir(exist_ok=True)

# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(DATASET_PATH)

print("\n" + "=" * 60)
print("       EXPLORATORY DATA ANALYSIS")
print("=" * 60)


# ============================================================
# 1. CHURN DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 6))

sns.countplot(
    data=df,
    x="Churn"
)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "churn_distribution.png",
    dpi=300
)

plt.close()

print("\n1. Churn distribution chart saved.")


# ============================================================
# 2. CHURN VS TENURE
# ============================================================

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="Churn",
    y="tenure"
)

plt.title("Customer Churn vs Tenure")
plt.xlabel("Churn")
plt.ylabel("Tenure (Months)")

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "churn_vs_tenure.png",
    dpi=300
)

plt.close()

print("2. Churn vs tenure chart saved.")


# ============================================================
# 3. CHURN VS MONTHLY CHARGES
# ============================================================

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="Churn",
    y="MonthlyCharges"
)

plt.title("Customer Churn vs Monthly Charges")
plt.xlabel("Churn")
plt.ylabel("Monthly Charges")

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "churn_vs_monthly_charges.png",
    dpi=300
)

plt.close()

print("3. Churn vs monthly charges chart saved.")


# ============================================================
# 4. CHURN BY CONTRACT TYPE
# ============================================================

plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="Contract",
    hue="Churn"
)

plt.title("Customer Churn by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Number of Customers")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "churn_by_contract.png",
    dpi=300
)

plt.close()

print("4. Churn by contract chart saved.")


# ============================================================
# 5. CHURN BY INTERNET SERVICE
# ============================================================

plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="InternetService",
    hue="Churn"
)

plt.title("Customer Churn by Internet Service")
plt.xlabel("Internet Service")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "churn_by_internet_service.png",
    dpi=300
)

plt.close()

print("5. Churn by internet service chart saved.")


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("       EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nCharts saved inside:")
print(RESULTS_DIR)