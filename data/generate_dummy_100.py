"""Generate a 100-row dummy Mall_Customers CSV matching the Kaggle dataset structure with stores."""
import pathlib
import numpy as np
import pandas as pd

import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from utils.stores import assign_stores_if_missing


def generate(n_per_cluster: int = 20, seed: int = 7) -> pd.DataFrame:
    np.random.seed(seed)
    n = n_per_cluster * 5

    customer_ids = range(1, n + 1)
    genders = np.random.choice(["Male", "Female"], size=n, p=[0.44, 0.56])
    ages = np.random.randint(18, 70, size=n)

    # 5 realistic segments (same ranges as the main generator)
    income_spending = []
    # Cluster 0: High income, high spending (Premium Spenders)
    for _ in range(n_per_cluster):
        income_spending.append((np.random.randint(70, 137), np.random.randint(63, 99)))
    # Cluster 1: High income, low spending (Careful Savers)
    for _ in range(n_per_cluster):
        income_spending.append((np.random.randint(68, 137), np.random.randint(1, 40)))
    # Cluster 2: Average income, average spending (Standard Customers)
    for _ in range(n_per_cluster):
        income_spending.append((np.random.randint(40, 70), np.random.randint(35, 65)))
    # Cluster 3: Low income, high spending (Impulse Buyers)
    for _ in range(n_per_cluster):
        income_spending.append((np.random.randint(15, 40), np.random.randint(60, 99)))
    # Cluster 4: Low income, low spending (Budget Shoppers)
    for _ in range(n_per_cluster):
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

    df = assign_stores_if_missing(df, seed=seed)
    return df


if __name__ == "__main__":
    df = generate()
    out = pathlib.Path(__file__).parent / "dummy_customers_100.csv"
    df.to_csv(out, index=False)
    print(f"Generated {len(df)} rows -> {out}")
