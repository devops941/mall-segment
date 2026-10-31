"""Store metadata, segment affinity assignments, and multi-tenant analytics."""

import numpy as np
import pandas as pd

STORE_METADATA = {
    "Apple Store": {
        "category": "Electronics",
        "icon": "🍎",
        "color": "#7C3AED",
        "strategy": (
            "Focus on premium flagship trade-ins, VIP pre-order experiences, and high-margin ecosystem "
            "accessories. Target tech-forward, high-income customers with personalized concierge demos."
        ),
    },
    "Zara": {
        "category": "Fashion & Apparel",
        "icon": "👗",
        "color": "#E11D48",
        "strategy": (
            "Curate high-fashion window displays, VIP fashion preview events, and time-limited runway collections. "
            "Leverage influencer-inspired styling guides to convert impulse-driven shoppers."
        ),
    },
    "H&M": {
        "category": "Fashion & Apparel",
        "icon": "👕",
        "color": "#F97316",
        "strategy": (
            "Promote student discounts, seasonal wardrobe refresh bundles, and app-exclusive reward points. "
            "Highlight sustainable, trendy basics for broad-appeal demographics."
        ),
    },
    "Food Court": {
        "category": "Dining",
        "icon": "🍔",
        "color": "#EAB308",
        "strategy": (
            "Introduce family lunch combo packs, student meal deals, and quick-serve QR ordering discounts. "
            "Run evening happy-hour promotions to capture cross-shopping footfall from apparel and cinema."
        ),
    },
    "PVR Cinemas": {
        "category": "Entertainment",
        "icon": "🍿",
        "color": "#8B5CF6",
        "strategy": (
            "Offer blockbuster movie ticket + snack combos, weekend family packages, and weekday afternoon discounts. "
            "Partner with surrounding restaurants for dinner-and-a-movie cross-promotions."
        ),
    },
    "Croma": {
        "category": "Electronics & Appliances",
        "icon": "📱",
        "color": "#06B6D4",
        "strategy": (
            "Highlight competitive price-match guarantees, extended warranty protection, and zero-cost EMI plans. "
            "Target quality-conscious savers looking for long-term appliance investments."
        ),
    },
    "Reliance Smart": {
        "category": "Groceries & Hypermarket",
        "icon": "🛒",
        "color": "#10B981",
        "strategy": (
            "Emphasize weekly grocery price slashes, buy-one-get-one essentials, and bulk-saving discounts. "
            "Drive repeat footfall through monthly loyalty cashback and essential household staples."
        ),
    },
}

STORE_NAMES = list(STORE_METADATA.keys())
STORE_CATEGORIES = {name: meta["category"] for name, meta in STORE_METADATA.items()}


def assign_stores_if_missing(
    df: pd.DataFrame,
    income_col: str = "Annual Income (k$)",
    score_col: str = "Spending Score (1-100)",
    seed: int = 42,
) -> pd.DataFrame:
    """Ensure dataframe has 'Store Visited' and 'Store Category' columns.
    
    If missing, assigns them realistically based on customer income and spending profiles.
    """
    df = df.copy()
    if "Store Visited" in df.columns and "Store Category" in df.columns:
        return df

    np.random.seed(seed)
    assigned_stores = []

    for _, row in df.iterrows():
        inc = row[income_col] if income_col in row else 50
        scr = row[score_col] if score_col in row else 50

        if inc >= 60 and scr >= 60:
            # Premium Spenders -> Heavy luxury electronics & high-end fashion
            probs = [0.35, 0.30, 0.05, 0.10, 0.15, 0.05, 0.00]
        elif inc >= 60 and scr < 50:
            # Careful Savers -> High research, electronics warranties, groceries
            probs = [0.08, 0.02, 0.05, 0.10, 0.15, 0.35, 0.25]
        elif inc < 45 and scr >= 55:
            # Impulse Buyers -> Fast fashion, dining, movies
            probs = [0.05, 0.30, 0.30, 0.20, 0.10, 0.00, 0.05]
        elif inc < 45 and scr < 45:
            # Budget Shoppers -> Essential groceries, discount stores
            probs = [0.00, 0.02, 0.13, 0.20, 0.10, 0.10, 0.45]
        else:
            # Standard Customers -> Balanced distribution
            probs = [0.05, 0.08, 0.22, 0.25, 0.20, 0.10, 0.10]

        probs = np.array(probs)
        probs /= probs.sum()
        store = np.random.choice(STORE_NAMES, p=probs)
        assigned_stores.append(store)

    df["Store Visited"] = assigned_stores
    df["Store Category"] = [STORE_CATEGORIES[s] for s in assigned_stores]
    return df

