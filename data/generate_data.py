"""Generate synthetic Mall_Customers.csv matching the Kaggle dataset structure with stores."""
import pathlib
import sys
import numpy as np
import pandas as pd

sys.path.append(str(pathlib.Path(__file__).parent.parent))
from utils.stores import assign_stores_if_missing

np.random.seed(42)
n = 200

customer_ids = range(1, n + 1)
genders = np.random.choice(["Male", "Female"], size=n, p=[0.44, 0.56])
ages = np.random.randint(18, 70, size=n)

# Create realistic clusters: 5 segments
income_spending = []
cluster_sizes = [40, 40, 40, 40, 40]

# Cluster 0: High income, high spending (Premium Spenders)
for _ in range(cluster_sizes[0]):
    income_spending.append((np.random.randint(70, 137), np.random.randint(63, 99)))

# Cluster 1: High income, low spending (Careful Savers)
for _ in range(cluster_sizes[1]):
    income_spending.append((np.random.randint(68, 137), np.random.randint(1, 40)))

# Cluster 2: Average income, average spending (Standard Customers)
for _ in range(cluster_sizes[2]):
    income_spending.append((np.random.randint(40, 70), np.random.randint(35, 65)))

# Cluster 3: Low income, high spending (Impulse Buyers)
for _ in range(cluster_sizes[3]):
    income_spending.append((np.random.randint(15, 40), np.random.randint(60, 99)))

# Cluster 4: Low income, low spending (Budget Shoppers)
for _ in range(cluster_sizes[4]):
    income_spending.append((np.random.randint(15, 40), np.random.randint(1, 40)))

np.random.shuffle(income_spending)
incomes = [x[0] for x in income_spending]
scores = [x[1] for x in income_spending]

df = pd.DataFrame({
    "CustomerID": customer_ids,
    "Gender": genders,
    "Age": ages,
    "Annual Income (k$)": incomes,
    "Spending Score (1-100)": scores,
})

df = assign_stores_if_missing(df, seed=42)

out = pathlib.Path(__file__).parent / "Mall_Customers.csv"
df.to_csv(out, index=False)
print(f"Generated {len(df)} rows -> {out}")

if __name__ == "__main__":
    pass
