# Mall Customer Segmentation & Multi-Store Tenant Analytics (KZ-ML-03)

An end-to-end unsupervised machine learning and retail business intelligence dashboard built with **Streamlit**, **Scikit-Learn**, and **Plotly**.

The project segments mall customers using **K-Means Clustering** based on Annual Income and Spending Score, justifies the cluster count using **Elbow (WCSS)** and **Silhouette Analysis**, maps mathematical clusters to actionable **marketing personas**, and provides multi-store **tenant analytics** (Overall Mall vs. Individual Store views).

---

## 🌟 Key Features

1. **Data Overview**:
   - High-level KPIs: Customer count, feature count, missing value checks, and store footprint.
   - Interactive dataframe inspection and statistical summaries (`describe()`).

2. **Exploratory Data Analysis (EDA)**:
   - Interactive visualizations for gender distribution (Donut chart), age distribution (Histogram), and bivariate scatter plots.
   - Numerical feature correlation heatmap using Seaborn/Matplotlib.

3. **Optimal Cluster Selection ($k$)**:
   - **Elbow Method (WCSS / Inertia)** evaluated across $k \in [1, 10]$.
   - **Silhouette Analysis** evaluated across $k \in [2, 10]$.
   - Algorithmic consensus indicating $k = 5$ as optimal.

4. **K-Means Clustering Engine**:
   - Interactive $k$-slider ($2 \le k \le 10$) with `k-means++` initialization.
   - Dynamic 2D scatter plot with black 'X' centroid overlays.
   - In-page store filtering option to isolate clusters by individual tenant stores.

5. **Customer Personas & Business Strategies**:
   - Automatic Euclidean distance matching of centroids to 5 retail customer personas:
     - 🔴 **Premium Spenders**: High Income, High Spending Score
     - 🔵 **Careful Savers**: High Income, Low Spending Score
     - 🟢 **Standard Customers**: Moderate Income, Moderate Spending Score
     - 🟠 **Impulse Buyers**: Low Income, High Spending Score
     - 🟣 **Budget Shoppers**: Low Income, Low Spending Score
   - Tailored marketing strategies for each segment and one-click segmented CSV export.

6. **Store-Level Mall Analytics (Multi-Tenant Drill-Down)**:
   - **Overall Mall View (Macro Tier)**: Footfall by store, category breakdown, store-wise spending & income comparisons, and stacked customer segment mix across stores.
   - **Individual Store View (Meso Tier)**: Drill-down into individual stores (Apple Store, Zara, H&M, Food Court, PVR Cinemas, Croma, Reliance Smart) with store-specific KPIs, customer positioning vs. overall mall background, segment share, demographics, custom marketing strategies, and store roster CSV download.

7. **Upload Your Data (BYOD)**:
   - Supports uploading custom customer CSV files with automated validation, clustering, profiling, and export.

---

## 🏗️ Project Architecture

```
mall_segment/
├── .streamlit/
│   └── config.toml                  # Violet/dark-sidebar theme configuration
├── data/
│   ├── Mall_Customers.csv           # 200 records with customer demographics and store visits
│   ├── dummy_customers_100.csv      # 100-row test dataset for upload validation
│   ├── generate_data.py             # Script to regenerate synthetic mall dataset
│   └── generate_dummy_100.py        # Script to generate 100-row test dataset
├── utils/
│   ├── __init__.py                  # Package initialization
│   ├── clustering.py                # K-Means, WCSS (Elbow), and Silhouette computations
│   ├── profiles.py                  # Persona bounding boxes, centroid-to-rule mapping
│   └── stores.py                    # Store metadata, categories, and segment affinity rules
├── app.py                           # 7-page interactive Streamlit dashboard
├── requirements.txt                 # Project dependencies
└── README.md                        # Documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Git

### 2. Installation
Clone the repository and install the dependencies:

```bash
git clone https://github.com/devops941/mall-segment.git
cd mall-segment
pip install -r requirements.txt
```

### 3. Run the Application
Launch the Streamlit dashboard locally:

```bash
streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.

---

## 📊 Dataset Schema

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `CustomerID` | Integer | Unique identifier for each customer (1 - 200) |
| `Gender` | String | Male / Female |
| `Age` | Integer | Customer age (18 - 70) |
| `Annual Income (k$)` | Integer | Customer annual income in thousands of dollars |
| `Spending Score (1-100)` | Integer | Mall-assigned score based on spending habits |
| `Store Visited` | String | Primary retail tenant visited (e.g. Zara, Apple Store, Food Court) |
| `Store Category` | String | Retail category (Electronics, Fashion, Dining, etc.) |

---

## 🛠️ Tech Stack

- **Frontend & App Framework**: Streamlit
- **Machine Learning**: Scikit-Learn (`KMeans`, `StandardScaler`, `silhouette_score`)
- **Data Manipulation**: Pandas, NumPy
- **Interactive Visualizations**: Plotly Express, Plotly Graph Objects
- **Statistical Graphics**: Seaborn, Matplotlib
