"""Mall Customer Segmentation -- Streamlit Dashboard (KZ-ML-03)."""

import pathlib

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

from utils.clustering import compute_wcss, compute_silhouette, run_kmeans, prepare_features
from utils.profiles import build_profiles, FALLBACK_COLORS
from utils.stores import (
    STORE_METADATA,
    STORE_NAMES,
    STORE_CATEGORIES,
    assign_stores_if_missing,
)

st.set_page_config(
    page_title="Mall Customer Segmentation",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = pathlib.Path(__file__).parent / "data" / "Mall_Customers.csv"

INCOME_COL = "Annual Income (k$)"
SCORE_COL = "Spending Score (1-100)"
AGE_COL = "Age"
GENDER_COL = "Gender"
STORE_COL = "Store Visited"
CAT_COL = "Store Category"


@st.cache_data
def load_default_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return assign_stores_if_missing(df)


def section_header(title: str, icon: str = "") -> None:
    prefix = f"{icon} " if icon else ""
    st.markdown(f"## {prefix}{title}")
    st.markdown("---")


# Sidebar
with st.sidebar:
    st.title("Mall Segment")
    st.caption("Mall Customer Segmentation & Tenant Analytics")
    st.divider()

    nav = st.radio(
        "Navigate",
        [
            "Data Overview",
            "Exploratory Analysis",
            "Optimal K",
            "Clustering",
            "Segment Profiles",
            "Store Analytics",
            "Upload Your Data",
        ],
        label_visibility="collapsed",
    )

    st.divider()



df_raw = load_default_data()


# ─── Page 1: Data Overview ───────────────────────────────────────────────────
if nav == "Data Overview":
    st.title("Mall Customer Segmentation")
    st.markdown(
        "An unsupervised K-Means clustering tool that groups mall customers by "
        "**Annual Income** and **Spending Score**, analyzes tenant/store-level behavior, "
        "and suggests targeted marketing strategies for each segment."
    )

    section_header("Dataset", "📋")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Customers", len(df_raw))
    col2.metric("Features", df_raw.shape[1])
    missing = int(df_raw.isnull().sum().sum())
    col3.metric("Missing Values", missing, delta="Clean" if missing == 0 else None)
    col4.metric("Genders", df_raw[GENDER_COL].nunique())
    col5.metric("Retail Stores", df_raw[STORE_COL].nunique() if STORE_COL in df_raw.columns else 0)

    st.dataframe(df_raw, width="stretch", height=420)

    section_header("Summary Statistics", "📊")
    st.dataframe(df_raw.describe().T.round(2), width="stretch")

    section_header("Missing Value Check", "🔍")
    miss = df_raw.isnull().sum().reset_index()
    miss.columns = ["Column", "Missing"]
    miss["Status"] = miss["Missing"].apply(lambda x: "OK" if x == 0 else f"{x} missing")
    st.dataframe(miss, width="stretch")


# ─── Page 2: Exploratory Analysis ────────────────────────────────────────────
elif nav == "Exploratory Analysis":
    section_header("Exploratory Data Analysis", "📈")

    c1, c2 = st.columns(2)

    with c1:
        gender_counts = df_raw[GENDER_COL].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig = px.pie(
            gender_counts,
            names="Gender",
            values="Count",
            title="Gender Distribution",
            color_discrete_sequence=["#3498db", "#e74c3c"],
            hole=0.35,
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, width="stretch")

    with c2:
        fig = px.histogram(
            df_raw,
            x=AGE_COL,
            nbins=20,
            title="Age Distribution",
            color_discrete_sequence=["#2ecc71"],
            labels={AGE_COL: "Age"},
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, width="stretch")

    st.markdown("### Annual Income vs Spending Score")
    hover_cols = ["CustomerID", AGE_COL]
    if STORE_COL in df_raw.columns:
        hover_cols.append(STORE_COL)
    if CAT_COL in df_raw.columns:
        hover_cols.append(CAT_COL)

    fig = px.scatter(
        df_raw,
        x=INCOME_COL,
        y=SCORE_COL,
        color=GENDER_COL,
        opacity=0.8,
        title="Annual Income vs Spending Score (by Gender)",
        color_discrete_map={"Male": "#3498db", "Female": "#e74c3c"},
        hover_data=hover_cols,
    )
    fig.update_traces(marker=dict(size=8))
    st.plotly_chart(fig, width="stretch")

    st.markdown("### Correlation Heatmap")
    numeric_df = df_raw.select_dtypes(include=np.number).drop(columns=["CustomerID"], errors="ignore")
    fig_h, ax = plt.subplots(figsize=(7, 4))
    sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax, linewidths=0.5)
    ax.set_title("Numerical Feature Correlation")
    st.pyplot(fig_h)
    plt.close(fig_h)


# ─── Page 3: Optimal K ───────────────────────────────────────────────────────
elif nav == "Optimal K":
    section_header("Finding the Optimal Number of Clusters (k)", "🎯")

    X_raw, X_fit, _ = prepare_features(df_raw, [INCOME_COL, SCORE_COL])

    with st.spinner("Computing WCSS and Silhouette scores..."):
        k_range = list(range(1, 11))
        wcss = compute_wcss(X_fit, k_range)
        sil_range = list(range(2, 11))
        sil_scores = compute_silhouette(X_fit, sil_range)

    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=k_range, y=wcss, mode="lines+markers",
            marker=dict(size=8, color="#e74c3c"),
            line=dict(color="#e74c3c", width=2),
        ))
        fig.add_vline(x=5, line_dash="dash", line_color="#3498db",
                      annotation_text="Elbow k=5", annotation_position="top right")
        fig.update_layout(
            title="Elbow Curve (WCSS)",
            xaxis_title="Number of Clusters (k)",
            yaxis_title="WCSS",
            plot_bgcolor="#f9f9f9",
        )
        st.plotly_chart(fig, width="stretch")

    with c2:
        best_k_idx = int(np.argmax(sil_scores))
        best_k = sil_range[best_k_idx]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=sil_range, y=sil_scores, mode="lines+markers",
            marker=dict(size=8, color="#2ecc71"),
            line=dict(color="#2ecc71", width=2),
        ))
        fig2.add_vline(x=best_k, line_dash="dash", line_color="#3498db",
                       annotation_text=f"Best k={best_k}", annotation_position="top right")
        fig2.update_layout(
            title="Silhouette Score",
            xaxis_title="Number of Clusters (k)",
            yaxis_title="Silhouette Score",
            plot_bgcolor="#f9f9f9",
        )
        st.plotly_chart(fig2, width="stretch")

    st.info(
        f"**Conclusion:** The Elbow curve bends at **k = 5**, and the Silhouette Score "
        f"peaks at **k = {best_k}**. Both methods agree -- use **k = 5** for segmentation."
    )

    col_a, col_b = st.columns(2)
    col_a.metric("Recommended k (Elbow)", 5)
    col_b.metric("Best Silhouette k", best_k, f"{max(sil_scores):.3f}")


# ─── Page 4: Clustering ──────────────────────────────────────────────────────
elif nav == "Clustering":
    section_header("K-Means Clustering", "🧩")

    col_ctrl1, col_ctrl2 = st.columns([1, 1])
    with col_ctrl1:
        k = st.slider("Select number of clusters (k)", min_value=2, max_value=10, value=5)
    with col_ctrl2:
        store_opts = ["🏢 All Stores (Overall Mall)"]
        if STORE_COL in df_raw.columns:
            store_opts += [f"{STORE_METADATA.get(s, {}).get('icon', '🛍️')} {s}" for s in sorted(df_raw[STORE_COL].dropna().unique())]
        selected_store_filter = st.selectbox("Store Filter (Highlight or filter by store)", store_opts)

    X_raw, X_fit, _ = prepare_features(df_raw, [INCOME_COL, SCORE_COL])

    with st.spinner(f"Running K-Means with k={k}..."):
        labels, centers, km = run_kmeans(X_fit, k)

    df_clustered = df_raw.copy()
    df_clustered["Cluster"] = labels.astype(str)

    # Apply store filter if selected
    is_filtered = selected_store_filter != "🏢 All Stores (Overall Mall)"
    if is_filtered:
        chosen_store = selected_store_filter.split(" ", 1)[1] if " " in selected_store_filter else selected_store_filter
        display_df = df_clustered[df_clustered[STORE_COL] == chosen_store]
        chart_title = f"K-Means Clusters (k={k}) -- Filtered for {chosen_store} ({len(display_df)} Customers)"
    else:
        display_df = df_clustered
        chart_title = f"K-Means Clusters (k={k}) -- Overall Mall ({len(display_df)} Customers)"

    colors = FALLBACK_COLORS[:k]

    hover_data_list = ["CustomerID", AGE_COL, GENDER_COL]
    if STORE_COL in display_df.columns:
        hover_data_list.append(STORE_COL)

    fig = px.scatter(
        display_df,
        x=INCOME_COL,
        y=SCORE_COL,
        color="Cluster",
        title=chart_title,
        color_discrete_sequence=colors,
        opacity=0.85,
        hover_data=hover_data_list,
    )

    for i, (cx, cy) in enumerate(centers):
        fig.add_trace(go.Scatter(
            x=[cx], y=[cy],
            mode="markers",
            marker=dict(symbol="x", size=16, color="black", line=dict(width=2)),
            name=f"Centroid {i}",
            showlegend=True,
        ))

    fig.update_layout(plot_bgcolor="#f9f9f9", legend_title="Cluster")
    st.plotly_chart(fig, width="stretch")

    st.markdown("### Cluster Summary")
    summary = (
        display_df.groupby("Cluster")[[INCOME_COL, SCORE_COL, AGE_COL]]
        .agg(["mean", "count"])
        .round(1)
    )
    st.dataframe(summary, width="stretch")

    st.metric("Total Model WCSS (Inertia)", f"{km.inertia_:.0f}")


# ─── Page 5: Segment Profiles ─────────────────────────────────────────────────
elif nav == "Segment Profiles":
    section_header("Segment Profiles & Marketing Strategies", "👥")

    X_raw, X_fit, _ = prepare_features(df_raw, [INCOME_COL, SCORE_COL])
    labels, centers, _ = run_kmeans(X_fit, 5)
    df_seg, profile_df = build_profiles(df_raw, labels, centers)

    for _, row in profile_df.iterrows():
        with st.expander(
            f"**{row['Segment']}** -- Cluster {int(row['Cluster'])} ({int(row['Count'])} customers)",
            expanded=True,
        ):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Avg Age", row["Avg Age"])
            c2.metric("Avg Income (k$)", row["Avg Income (k$)"])
            c3.metric("Avg Spending Score", row["Avg Spending Score"])
            c4.metric("Customers", int(row["Count"]))
            st.markdown(f"**Marketing Strategy:** {row['Strategy']}")

    st.markdown("### Segment Distribution")
    fig = px.bar(
        profile_df,
        x="Segment",
        y="Count",
        color="Segment",
        color_discrete_sequence=[r["Color"] for _, r in profile_df.iterrows()],
        title="Customer Count per Segment",
        text="Count",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, plot_bgcolor="#f9f9f9")
    st.plotly_chart(fig, width="stretch")

    st.markdown("### Income vs Spending by Segment")
    color_map = {row["Segment"]: row["Color"] for _, row in profile_df.iterrows()}
    
    hover_items = ["CustomerID", AGE_COL, GENDER_COL]
    if STORE_COL in df_seg.columns:
        hover_items.append(STORE_COL)
        
    fig2 = px.scatter(
        df_seg,
        x=INCOME_COL,
        y=SCORE_COL,
        color="Segment",
        color_discrete_map=color_map,
        title="Segments -- Income vs Spending Score",
        opacity=0.8,
        hover_data=hover_items,
    )
    fig2.update_layout(plot_bgcolor="#f9f9f9")
    st.plotly_chart(fig2, width="stretch")

    st.markdown("### Download Segmented Dataset")
    csv_out = df_seg.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV with Segments",
        data=csv_out,
        file_name="mall_customers_segmented.csv",
        mime="text/csv",
    )


# ─── Page 6: Store Analytics (New Dedicated Page!) ────────────────────────────
elif nav == "Store Analytics":
    section_header("Store-Level Mall Analytics", "🏬")
    st.markdown(
        "Explore shopping patterns across individual tenant stores. Analyze the entire mall's "
        "footfall and segment distributions collectively, or drill down into specific stores "
        "to inspect customer personas, demographics, and store-specific marketing strategies."
    )

    # Fit k=5 baseline clustering to have segments attached
    X_raw, X_fit, _ = prepare_features(df_raw, [INCOME_COL, SCORE_COL])
    labels, centers, _ = run_kmeans(X_fit, 5)
    df_seg, profile_df = build_profiles(df_raw, labels, centers)

    color_map = {row["Segment"]: row["Color"] for _, row in profile_df.iterrows()}

    # Store selector
    store_options = ["🏢 All Stores (Overall Mall View)"] + [
        f"{STORE_METADATA.get(s, {}).get('icon', '🛍️')} {s}" for s in STORE_NAMES if s in df_seg[STORE_COL].values
    ]

    selected_store_raw = st.selectbox(
        "Select Store View",
        store_options,
        index=0,
        help="Select 'All Stores' for the overall macro view, or pick an individual store to drill down.",
    )

    is_overall = selected_store_raw == "🏢 All Stores (Overall Mall View)"

    # ── VIEW A: Overall Mall View ─────────────────────────────────────────────
    if is_overall:
        st.markdown("### 🏢 Overall Mall Tenant Analytics")

        # Top KPI Metrics
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Stores", df_seg[STORE_COL].nunique())
        kpi2.metric("Total Shoppers", len(df_seg))

        store_counts = df_seg[STORE_COL].value_counts()
        top_traffic_store = store_counts.index[0]
        top_traffic_count = store_counts.iloc[0]
        kpi3.metric("Highest Footfall", f"{top_traffic_store} ({top_traffic_count})")

        store_avg_spend = df_seg.groupby(STORE_COL)[SCORE_COL].mean().round(1)
        top_spend_store = store_avg_spend.idxmax()
        top_spend_val = store_avg_spend.max()
        kpi4.metric("Top Avg Spending Store", f"{top_spend_store} ({top_spend_val}/100)")

        st.divider()

        # Row 1: Footfall & Category Distribution
        c1, c2 = st.columns(2)

        with c1:
            footfall_df = df_seg[STORE_COL].value_counts().reset_index()
            footfall_df.columns = ["Store", "Customer Count"]
            store_color_seq = [
                STORE_METADATA.get(s, {}).get("color", "#7C3AED") for s in footfall_df["Store"]
            ]

            fig_footfall = px.bar(
                footfall_df,
                x="Store",
                y="Customer Count",
                color="Store",
                color_discrete_sequence=store_color_seq,
                title="Customer Footfall per Store",
                text="Customer Count",
            )
            fig_footfall.update_traces(textposition="outside")
            fig_footfall.update_layout(showlegend=False, plot_bgcolor="#f9f9f9")
            st.plotly_chart(fig_footfall, width="stretch")

        with c2:
            cat_df = df_seg[CAT_COL].value_counts().reset_index()
            cat_df.columns = ["Category", "Shoppers"]
            fig_cat = px.pie(
                cat_df,
                names="Category",
                values="Shoppers",
                title="Shopper Distribution by Retail Category",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_cat.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_cat, width="stretch")

        # Row 2: Average Spending Score & Average Income Comparison
        c3, c4 = st.columns(2)

        with c3:
            spend_df = df_seg.groupby(STORE_COL)[SCORE_COL].mean().round(1).reset_index()
            spend_df.columns = ["Store", "Avg Spending Score"]
            spend_df = spend_df.sort_values(by="Avg Spending Score", ascending=False)

            fig_spend = px.bar(
                spend_df,
                x="Store",
                y="Avg Spending Score",
                color="Avg Spending Score",
                color_continuous_scale="Viridis",
                title="Average Spending Score by Store",
                text="Avg Spending Score",
            )
            fig_spend.update_traces(textposition="outside")
            fig_spend.update_layout(plot_bgcolor="#f9f9f9")
            st.plotly_chart(fig_spend, width="stretch")

        with c4:
            inc_df = df_seg.groupby(STORE_COL)[INCOME_COL].mean().round(1).reset_index()
            inc_df.columns = ["Store", "Avg Income (k$)"]
            inc_df = inc_df.sort_values(by="Avg Income (k$)", ascending=False)

            fig_inc = px.bar(
                inc_df,
                x="Store",
                y="Avg Income (k$)",
                color="Avg Income (k$)",
                color_continuous_scale="Purples",
                title="Average Annual Customer Income by Store (k$)",
                text="Avg Income (k$)",
            )
            fig_inc.update_traces(textposition="outside")
            fig_inc.update_layout(plot_bgcolor="#f9f9f9")
            st.plotly_chart(fig_inc, width="stretch")

        # Row 3: Cross-Store Customer Segment Distribution (Stacked Bar Chart)
        st.markdown("### 🧬 Customer Segment Mix Across Stores")
        cross_df = df_seg.groupby([STORE_COL, "Segment"]).size().reset_index(name="Count")

        fig_cross = px.bar(
            cross_df,
            x=STORE_COL,
            y="Count",
            color="Segment",
            title="Customer Segment Breakdown per Store (Stacked)",
            color_discrete_map=color_map,
            barmode="stack",
            text="Count",
        )
        fig_cross.update_layout(plot_bgcolor="#f9f9f9", legend_title="Customer Segment")
        st.plotly_chart(fig_cross, width="stretch")

        # Tenant Summary Benchmark Table
        st.markdown("### 📋 Tenant Performance Benchmark Table")
        tenant_summary = []
        for store in sorted(df_seg[STORE_COL].unique()):
            st_sub = df_seg[df_seg[STORE_COL] == store]
            dominant_seg = st_sub["Segment"].value_counts().index[0]
            cat = st_sub[CAT_COL].iloc[0] if CAT_COL in st_sub else STORE_CATEGORIES.get(store, "General")
            tenant_summary.append({
                "Store Name": store,
                "Category": cat,
                "Shoppers": len(st_sub),
                "% Mall Footfall": f"{round((len(st_sub) / len(df_seg)) * 100, 1)}%",
                "Avg Age": round(st_sub[AGE_COL].mean(), 1),
                "Avg Income (k$)": round(st_sub[INCOME_COL].mean(), 1),
                "Avg Spending Score": round(st_sub[SCORE_COL].mean(), 1),
                "Dominant Segment": dominant_seg,
            })
        st.dataframe(pd.DataFrame(tenant_summary), width="stretch")

    # ── VIEW B: Individual Store Drill-Down View ──────────────────────────────
    else:
        # Extract clean store name
        curr_store = selected_store_raw.split(" ", 1)[1] if " " in selected_store_raw else selected_store_raw
        store_df = df_seg[df_seg[STORE_COL] == curr_store]
        meta = STORE_METADATA.get(curr_store, {})

        st.markdown(
            f"### {meta.get('icon', '🛍️')} {curr_store} -- Store Deep-Dive Analytics"
        )
        st.caption(f"**Category:** {meta.get('category', 'Retail')}  |  **Store Color Code:** `{meta.get('color', '#7C3AED')}`")

        # Store-Specific KPI Cards
        skpi1, skpi2, skpi3, skpi4 = st.columns(4)
        footfall_pct = round((len(store_df) / len(df_seg)) * 100, 1)
        skpi1.metric("Store Shoppers", len(store_df), delta=f"{footfall_pct}% of Mall")
        skpi2.metric("Avg Customer Age", f"{store_df[AGE_COL].mean():.1f} yrs")
        skpi3.metric("Avg Annual Income", f"${store_df[INCOME_COL].mean():.1f}k")
        skpi4.metric("Avg Spending Score", f"{store_df[SCORE_COL].mean():.1f} / 100")

        st.divider()

        # Visualizations Row 1: Customer Positioning vs Mall Background & Segment Share
        sc1, sc2 = st.columns(2)

        with sc1:
            # Scatter plot with all mall customers in background and store highlighted
            fig_pos = go.Figure()

            # Background: Other mall shoppers
            other_df = df_seg[df_seg[STORE_COL] != curr_store]
            fig_pos.add_trace(go.Scatter(
                x=other_df[INCOME_COL],
                y=other_df[SCORE_COL],
                mode="markers",
                marker=dict(size=6, color="#d1d5db", opacity=0.4),
                name="Other Mall Shoppers",
                hoverinfo="skip",
            ))

            # Foreground: This store's shoppers by segment
            for seg_name, seg_color in color_map.items():
                seg_sub = store_df[store_df["Segment"] == seg_name]
                if not seg_sub.empty:
                    fig_pos.add_trace(go.Scatter(
                        x=seg_sub[INCOME_COL],
                        y=seg_sub[SCORE_COL],
                        mode="markers",
                        marker=dict(size=11, color=seg_color, line=dict(width=1, color="black")),
                        name=seg_name,
                        text=[
                            f"ID: {r.CustomerID}<br>Age: {r.Age}<br>Gender: {r.Gender}<br>Segment: {r.Segment}"
                            for _, r in seg_sub.iterrows()
                        ],
                        hoverinfo="text",
                    ))

            fig_pos.update_layout(
                title=f"{curr_store} Customers vs. Overall Mall",
                xaxis_title=INCOME_COL,
                yaxis_title=SCORE_COL,
                plot_bgcolor="#f9f9f9",
                legend_title="Customer Segment",
            )
            st.plotly_chart(fig_pos, width="stretch")

        with sc2:
            store_seg_counts = store_df["Segment"].value_counts().reset_index()
            store_seg_counts.columns = ["Segment", "Count"]

            fig_store_seg = px.pie(
                store_seg_counts,
                names="Segment",
                values="Count",
                title=f"{curr_store} Customer Segment Distribution",
                hole=0.45,
                color="Segment",
                color_discrete_map=color_map,
            )
            fig_store_seg.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_store_seg, width="stretch")

        # Visualizations Row 2: Age Histogram & Gender Ratio for this store
        sc3, sc4 = st.columns(2)

        with sc3:
            fig_age = px.histogram(
                store_df,
                x=AGE_COL,
                nbins=12,
                title=f"{curr_store} Customer Age Distribution",
                color_discrete_sequence=[meta.get("color", "#7C3AED")],
                labels={AGE_COL: "Age"},
            )
            fig_age.add_vline(
                x=store_df[AGE_COL].mean(),
                line_dash="dash",
                line_color="#e74c3c",
                annotation_text=f"Mean: {store_df[AGE_COL].mean():.1f} yrs",
            )
            fig_age.update_layout(bargap=0.1, plot_bgcolor="#f9f9f9")
            st.plotly_chart(fig_age, width="stretch")

        with sc4:
            store_gender = store_df[GENDER_COL].value_counts().reset_index()
            store_gender.columns = ["Gender", "Count"]
            fig_sgender = px.pie(
                store_gender,
                names="Gender",
                values="Count",
                title=f"{curr_store} Gender Ratio",
                hole=0.4,
                color_discrete_sequence=["#3498db", "#e74c3c"],
            )
            fig_sgender.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_sgender, width="stretch")

        # Tailored Marketing Recommendation
        st.markdown("### 💡 Tailored Store Marketing Strategy")
        dominant_segment = store_df["Segment"].value_counts().index[0]
        dom_pct = round((store_df["Segment"].value_counts().iloc[0] / len(store_df)) * 100, 1)

        st.success(
            f"**Dominant Customer Segment:** `{dominant_segment}` ({dom_pct}% of {curr_store}'s footfall)\n\n"
            f"**Actionable Marketing Recommendation:**\n\n"
            f"{meta.get('strategy', 'Analyze shopper frequency and deliver personalized rewards.')}"
        )

        # Customer List & Export
        st.markdown(f"### 👥 {curr_store} Customer Roster")
        cols_to_show = ["CustomerID", GENDER_COL, AGE_COL, INCOME_COL, SCORE_COL, "Segment"]
        st.dataframe(store_df[cols_to_show].reset_index(drop=True), width="stretch")

        store_csv = store_df[cols_to_show].to_csv(index=False).encode("utf-8")
        st.download_button(
            f"Download {curr_store} Customer Data",
            data=store_csv,
            file_name=f"{curr_store.lower().replace(' ', '_')}_customers.csv",
            mime="text/csv",
        )


# ─── Page 7: Upload Your Data ─────────────────────────────────────────────────
elif nav == "Upload Your Data":
    section_header("Upload & Segment Your Own Data", "📤")

    st.markdown(
        "Upload a CSV containing at least **Annual Income (k$)** and "
        "**Spending Score (1-100)** columns. The app will cluster it and "
        "let you download the results."
    )

    uploaded = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded is not None:
        try:
            df_up = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Could not read file: {e}")
            st.stop()

        required = [INCOME_COL, SCORE_COL]
        missing_cols = [c for c in required if c not in df_up.columns]
        if missing_cols:
            st.error(
                f"Missing required column(s): **{', '.join(missing_cols)}**. "
                "Please ensure your CSV has these exact column names."
            )
            st.stop()

        # If Store Visited is not present, auto-assign it realistically so store analytics work smoothly
        df_up = assign_stores_if_missing(df_up)

        st.success(f"Loaded {len(df_up)} rows with {df_up.shape[1]} columns.")
        st.dataframe(df_up.head(), width="stretch")

        k_up = st.slider("Select k for clustering", 2, 10, 5, key="upload_k")

        if st.button("Run Segmentation"):
            with st.spinner("Clustering..."):
                X_up, X_up_fit, _ = prepare_features(df_up, [INCOME_COL, SCORE_COL])
                labels_up, centers_up, _ = run_kmeans(X_up_fit, k_up)
                df_result, profile_up = build_profiles(df_up, labels_up, centers_up)

            st.markdown("### Cluster Results")
            fig = px.scatter(
                df_result,
                x=INCOME_COL,
                y=SCORE_COL,
                color="Segment",
                title=f"Your Data -- {k_up} Segments",
                opacity=0.8,
                hover_data=[c for c in ["CustomerID", AGE_COL, GENDER_COL, STORE_COL] if c in df_result.columns],
            )
            st.plotly_chart(fig, width="stretch")

            st.markdown("### Segment Profiles")
            st.dataframe(
                profile_up[["Cluster", "Segment", "Count", "Avg Income (k$)", "Avg Spending Score", "Strategy"]],
                width="stretch",
            )

            csv_dl = df_result.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Segmented Results",
                data=csv_dl,
                file_name="your_customers_segmented.csv",
                mime="text/csv",
            )
    else:
        st.info("No file uploaded yet. Test with the default dataset from the other pages.")
        st.markdown("**Expected CSV format:**")
        sample = pd.DataFrame({
            "CustomerID": [1, 2, 3],
            INCOME_COL: [85, 32, 61],
            SCORE_COL: [78, 25, 55],
        })
        st.dataframe(sample, width="stretch")
