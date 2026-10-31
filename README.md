# Mall Customer Segmentation & Multi-Store Tenant Analytics (KZ-ML-03)

An end-to-end unsupervised machine learning and retail business intelligence dashboard built with **Streamlit**, **Scikit-Learn**, **Plotly**, and **PostgreSQL**.

The project segments mall customers using **K-Means Clustering** based on Annual Income and Spending Score, justifies the cluster count using **Elbow (WCSS)** and **Silhouette Analysis**, maps mathematical clusters to actionable **marketing personas**, and provides multi-store **tenant analytics** (Overall Mall vs. Individual Store views).

It is now **multi-tenant**: the mall owner (admin) sees the whole mall, and each tenant store signs in to enter and analyze only its own customers.

---

## 🔐 Roles & Access

| Role | Sees | Can do |
| :--- | :--- | :--- |
| **Mall Owner (Admin)** | The entire mall (all stores, live) | Approve/reject stores, create stores, reset & email credentials, delete stores, full analytics, CSV upload |
| **Store** | Only its own customers | Manually enter/edit/delete its customer records, run analytics on its own data |

### Store onboarding — two paths
1. **Store self-registers** → account is created as `pending` → the mall admin approves or rejects it → store signs in.
2. **Admin creates the store** → credentials are generated and **emailed to the store**, account is approved immediately.

Admin can also **reset a store password** (emailed) and **disable** a store at any time.

### Data entry
Stores enter customers **manually** through a form (gender, age, annual income, spending score) — no CSV upload for stores. Every entry is saved to the database immediately and becomes visible to the mall owner in the overall-mall view.

---

## 🌟 Key Features

1. **Authentication**: Admin login, store login, and store self-registration with approval workflow.
2. **Data Overview**: KPIs, interactive dataframe inspection, and statistical summaries, scoped to the signed-in role.
3. **Exploratory Data Analysis (EDA)**: Gender donut, age histogram, bivariate scatter, and a correlation heatmap.
4. **Optimal Cluster Selection ($k$)**: Elbow (WCSS) and Silhouette analysis, computed dynamically from the current data (with a sample-aware max $k$).
5. **K-Means Clustering Engine**: Interactive $k$-slider with `k-means++` init, centroid overlays, and store filtering.
6. **Customer Personas & Business Strategies**: Automatic centroid-to-persona mapping (Premium Spenders, Careful Savers, Standard Customers, Impulse Buyers, Budget Shoppers) with tailored strategies and CSV export.
7. **Store Analytics**: Overall mall macro view (footfall, category mix, store comparisons, cross-store segment mix) and per-store drill-down.
8. **Store Management (admin)**: Pending approvals, store creation with emailed credentials, password resets, enable/disable, and deletion.
9. **My Data Entry (store)**: Manual customer entry with live record table and delete.
10. **Upload Your Data (admin)**: Optional CSV upload for ad-hoc segmentation.

---

## 🏗️ Project Architecture

```
mall_segment/
├── .streamlit/
│   └── config.toml                  # Violet/dark-sidebar theme configuration
├── data/
│   ├── Mall_Customers.csv           # 200 records used to seed the database
│   ├── dummy_customers_100.csv      # 100-row sample for upload testing
│   ├── generate_data.py             # Script to regenerate the synthetic dataset
│   └── generate_dummy_100.py        # Script to generate the 100-row dataset
├── utils/
│   ├── __init__.py                  # Package initialization
│   ├── auth.py                      # Password hashing (bcrypt), JWT tokens, admin check
│   ├── clustering.py                # K-Means, WCSS (Elbow), and Silhouette computations
│   ├── db.py                        # SQLAlchemy models, sessions, and data access
│   ├── mailer.py                    # SMTP delivery of credentials and notifications
│   ├── profiles.py                  # Persona bounding boxes, centroid-to-rule mapping
│   └── stores.py                    # Store metadata, categories, and segment affinity rules
├── app.py                           # Multi-tenant Streamlit dashboard
├── requirements.txt                 # Project dependencies
├── .env                             # Secrets (NOT committed)
└── README.md                        # Documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- A PostgreSQL database (this project is configured for [Neon](https://neon.tech))

### 2. Configuration
Create a `.env` file in the project root:

```ini
DATABASE_URL="postgresql://<user>:<password>@<host>/<db>?sslmode=require"
JWT_SECRET="<random-hex-secret>"

ADMIN_EMAIL="<owner-login-email>"
ADMIN_PASSWORD="<owner-login-password>"

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<smtp-user>
SMTP_PASS=<smtp-app-password>
SMTP_FROM=<smtp-from>
FROM_NAME=<sender-name>

# Optional — sign-in screen help. Leave unset in production.
SHOW_DEMO_CREDENTIALS=true
```

`.env` is git-ignored — never commit real credentials. The owner signs in with
whatever you set for `ADMIN_EMAIL` / `ADMIN_PASSWORD`; nothing is hardcoded in
the app.

`SHOW_DEMO_CREDENTIALS` renders a small "demo credentials" panel under the
sign-in form. Set it only on local or demo deployments; when it is unset the
panel never renders, so production shows nothing.

When the flag is on, the app also creates three ready-to-use demo stores (each
with a few sample shoppers) the first time the sign-in screen loads:

| Store | Email | Password |
| --- | --- | --- |
| Demo Store — Fashion | `demo.fashion@mallsegment.local` | `demo1234` |
| Demo Store — Electronics | `demo.electronics@mallsegment.local` | `demo1234` |
| Demo Store — Grocery | `demo.grocery@mallsegment.local` | `demo1234` |

These are created only when `SHOW_DEMO_CREDENTIALS` is enabled, so a production
deployment never gets them.

### 3. Installation
```bash
git clone https://github.com/devops941/mall-segment.git
cd mall-segment
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

On first launch the app creates its tables and seeds the 7 tenant stores and the
200-row demo dataset, so the dashboard looks populated immediately.

Sign in as admin with `ADMIN_EMAIL` / `ADMIN_PASSWORD`, or create a store from
the **Store Management** page.

---

## 📊 Dataset Schema

Customer records (stored in the `customers` table):

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `CustomerID` | Integer | Unique identifier (database primary key) |
| `Gender` | String | Male / Female / Other |
| `Age` | Integer | Customer age |
| `Annual Income (k$)` | Float | Customer annual income in thousands of dollars |
| `Spending Score (1-100)` | Float | Mall-assigned score based on spending habits |
| `Store Visited` | String | Owning retail tenant |
| `Store Category` | String | Retail category (Electronics, Fashion, Dining, etc.) |

Store accounts (stored in the `stores` table): name, email, category, icon,
color, password hash, status (`pending` / `approved` / `rejected` / `disabled`),
creator (`self` / `admin` / `seed`), and timestamps.

---

## 🛠️ Tech Stack

- **Frontend & App Framework**: Streamlit
- **Machine Learning**: Scikit-Learn (`KMeans`, `StandardScaler`, `silhouette_score`)
- **Database**: PostgreSQL (Neon) via SQLAlchemy + psycopg2
- **Auth**: bcrypt + PyJWT
- **Email**: SMTP (Gmail)
- **Data Manipulation**: Pandas, NumPy
- **Interactive Visualizations**: Plotly Express, Plotly Graph Objects
- **Statistical Graphics**: Seaborn, Matplotlib


