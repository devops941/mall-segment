import pandas as pd

SEGMENT_RULES = [
    {
        "name": "Premium Spenders",
        "income_min": 60,
        "income_max": 200,
        "score_min": 60,
        "score_max": 100,
        "color": "#e74c3c",
        "strategy": (
            "Offer loyalty programmes, exclusive early-access previews, and VIP events. "
            "Focus on premium brands and personalised recommendations."
        ),
    },
    {
        "name": "Careful Savers",
        "income_min": 60,
        "income_max": 200,
        "score_min": 0,
        "score_max": 45,
        "color": "#3498db",
        "strategy": (
            "Emphasise quality, value, and long-term durability. Use email newsletters "
            "highlighting best-in-class products and investment pieces."
        ),
    },
    {
        "name": "Standard Customers",
        "income_min": 35,
        "income_max": 70,
        "score_min": 35,
        "score_max": 65,
        "color": "#2ecc71",
        "strategy": (
            "Regular seasonal promotions, bundle deals, and loyalty points. "
            "Broad-appeal campaigns with moderate discounts."
        ),
    },
    {
        "name": "Impulse Buyers",
        "income_min": 0,
        "income_max": 45,
        "score_min": 55,
        "score_max": 100,
        "color": "#f39c12",
        "strategy": (
            "Flash sales, combo deals, EMI/instalment offers, and limited-time discounts. "
            "In-store displays and social media impulse triggers."
        ),
    },
    {
        "name": "Budget Shoppers",
        "income_min": 0,
        "income_max": 45,
        "score_min": 0,
        "score_max": 45,
        "color": "#9b59b6",
        "strategy": (
            "Discount days, clearance sales, and value packs. "
            "Focus on essential items and price-matching campaigns."
        ),
    },
]

CLUSTER_COLORS = [r["color"] for r in SEGMENT_RULES]
FALLBACK_COLORS = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
                   "#1abc9c", "#e67e22", "#34495e"]


def _centroid_to_rule(income_mean: float, score_mean: float) -> dict:
    best = None
    best_dist = float("inf")
    for rule in SEGMENT_RULES:
        ci = (rule["income_min"] + rule["income_max"]) / 2
        cs = (rule["score_min"] + rule["score_max"]) / 2
        dist = (income_mean - ci) ** 2 + (score_mean - cs) ** 2
        if dist < best_dist:
            best_dist = dist
            best = rule
    return best


def build_profiles(df: pd.DataFrame, labels, centers) -> pd.DataFrame:
    df = df.copy()
    df["Cluster"] = labels

    rows = []
    used_names: set[str] = set()

    for i, center in enumerate(centers):
        subset = df[df["Cluster"] == i]
        income_col = "Annual Income (k$)"
        score_col = "Spending Score (1-100)"

        income_mean = center[0] if len(center) >= 1 else subset[income_col].mean()
        score_mean = center[1] if len(center) >= 2 else subset[score_col].mean()

        rule = _centroid_to_rule(income_mean, score_mean)
        name = rule["name"]
        # avoid duplicates when k differs from 5
        suffix = 2
        base = name
        while name in used_names:
            name = f"{base} {suffix}"
            suffix += 1
        used_names.add(name)

        rows.append(
            {
                "Cluster": i,
                "Segment": name,
                "Count": len(subset),
                "Avg Age": round(subset["Age"].mean(), 1) if "Age" in subset else "-",
                "Avg Income (k$)": round(income_mean, 1),
                "Avg Spending Score": round(score_mean, 1),
                "Strategy": rule["strategy"],
                "Color": rule["color"],
            }
        )

    df["Segment"] = df["Cluster"].map({r["Cluster"]: r["Segment"] for r in rows})
    return df, pd.DataFrame(rows)


def get_color_map(profile_df: pd.DataFrame) -> dict:
    return dict(zip(profile_df["Cluster"], profile_df["Color"]))
