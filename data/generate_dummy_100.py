"""Generate realistic synthetic dummy_customers_100.csv (100 records).

Used for testing the Upload & Bring-Your-Own-Data workflow in Streamlit.
"""

import pathlib
import numpy as np
import pandas as pd

STORE_CATEGORIES = {
    "Apple Store": "Electronics",
    "Zara": "Fashion & Apparel",
    "H&M": "Fashion & Apparel",
    "Food Court": "Dining",
    "PVR Cinemas": "Entertainment",
    "Croma": "Electronics & Appliances",
    "Reliance Smart": "Groceries & Hypermarket",
}


def generate_dataset(n: int = 100, seed: int = 7) -> pd.DataFrame:
    np.random.seed(seed)
    n_per_segment = n // 5

    records = []

    # 1. Premium Spenders (High Income, High Spending)
    for _ in range(n_per_segment):
        gender = np.random.choice(["Female", "Male"], p=[0.55, 0.45])
        age = int(np.random.randint(24, 45))
        income = int(np.random.randint(72, 137))
        score = int(np.random.randint(68, 99))
        store = np.random.choice(["Apple Store", "Zara", "PVR Cinemas"], p=[0.50, 0.40, 0.10])
        records.append({
            "Gender": gender,
            "Age": age,
            "Annual Income (k$)": income,
            "Spending Score (1-100)": score,
            "Store Visited": store,
            "Store Category": STORE_CATEGORIES[store],
        })

    # 2. Careful Savers (High Income, Low Spending)
    for _ in range(n_per_segment):
        gender = np.random.choice(["Female", "Male"], p=[0.50, 0.50])
        age = int(np.random.randint(35, 65))
        income = int(np.random.randint(70, 137))
        score = int(np.random.randint(6, 40))
        store = np.random.choice(["Croma", "Reliance Smart", "Apple Store"], p=[0.55, 0.35, 0.10])
        records.append({
            "Gender": gender,
            "Age": age,
            "Annual Income (k$)": income,
            "Spending Score (1-100)": score,
            "Store Visited": store,
            "Store Category": STORE_CATEGORIES[store],
        })

    # 3. Standard Customers (Average Income, Average Spending)
    for _ in range(n_per_segment):
        gender = np.random.choice(["Female", "Male"], p=[0.55, 0.45])
        age = int(np.random.randint(22, 58))
        income = int(np.random.randint(42, 69))
        score = int(np.random.randint(38, 65))
        store = np.random.choice(["Food Court", "PVR Cinemas", "H&M", "Croma"], p=[0.35, 0.30, 0.25, 0.10])
        records.append({
            "Gender": gender,
            "Age": age,
            "Annual Income (k$)": income,
            "Spending Score (1-100)": score,
            "Store Visited": store,
            "Store Category": STORE_CATEGORIES[store],
        })

    # 4. Impulse Buyers (Low Income, High Spending)
    for _ in range(n_per_segment):
        gender = np.random.choice(["Female", "Male"], p=[0.60, 0.40])
        age = int(np.random.randint(18, 33))
        income = int(np.random.randint(15, 40))
        score = int(np.random.randint(65, 99))
        store = np.random.choice(["H&M", "Zara", "Food Court"], p=[0.50, 0.35, 0.15])
        records.append({
            "Gender": gender,
            "Age": age,
            "Annual Income (k$)": income,
            "Spending Score (1-100)": score,
            "Store Visited": store,
            "Store Category": STORE_CATEGORIES[store],
        })

    # 5. Budget Shoppers (Low Income, Low Spending)
    for _ in range(n_per_segment):
        gender = np.random.choice(["Female", "Male"], p=[0.52, 0.48])
        age = int(np.random.randint(20, 68))
        income = int(np.random.randint(15, 40))
        score = int(np.random.randint(5, 42))
        store = np.random.choice(["Reliance Smart", "Food Court", "Croma"], p=[0.60, 0.30, 0.10])
        records.append({
            "Gender": gender,
            "Age": age,
            "Annual Income (k$)": income,
            "Spending Score (1-100)": score,
            "Store Visited": store,
            "Store Category": STORE_CATEGORIES[store],
        })

    df = pd.DataFrame(records)
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    df.insert(0, "CustomerID", range(1, len(df) + 1))
    return df


if __name__ == "__main__":
    df = generate_dataset(100, seed=7)
    out_path = pathlib.Path(__file__).parent / "dummy_customers_100.csv"
    df.to_csv(out_path, index=False)
    print(f"Generated clean {len(df)} rows -> {out_path}")
