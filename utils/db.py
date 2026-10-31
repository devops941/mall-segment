"""Database layer for multi-tenant mall analytics.

Provides SQLAlchemy models (Store, Customer), session management, and the
data-access helpers used by the Streamlit app. The app talks to Neon Postgres
through DATABASE_URL; the demo CSV is only used once, to seed the database.
"""

from __future__ import annotations

import os
import pathlib
import re
from contextlib import contextmanager
from datetime import datetime, timezone

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

_ROOT = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")

# Column order the rest of the app expects when it reads customer data.
CUSTOMER_COLUMNS = [
    "CustomerID",
    "Gender",
    "Age",
    "Annual Income (k$)",
    "Spending Score (1-100)",
    "Store Visited",
    "Store Category",
]

STORE_STATUSES = ("pending", "approved", "rejected", "disabled")


def _get_secret(key: str, default: str = "") -> str:
    val = os.getenv(key, "")
    if not val:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and key in st.secrets:
                val = str(st.secrets[key])
        except Exception:
            pass
    return (val or default).strip()


def _normalize_url(url: str) -> str:
    # SQLAlchemy 2.x defaults to the psycopg3 driver; the URL points at psycopg2.
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


def get_database_url() -> str:
    url = _get_secret("DATABASE_URL", "")
    if not url:
        db_path = _ROOT / "mall_segment.db"
        url = f"sqlite:///{db_path}"
    return _normalize_url(url)


DATABASE_URL = get_database_url()
Base = declarative_base()


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    category = Column(String(120), default="General")
    icon = Column(String(16), default="🛍️")
    color = Column(String(16), default="#7C3AED")
    password_hash = Column(String(200), nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    created_by = Column(String(20), default="self")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    approved_at = Column(DateTime(timezone=True), nullable=True)

    customers = relationship("Customer", back_populates="store", cascade="all, delete-orphan")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    gender = Column(String(16))
    age = Column(Integer)
    annual_income = Column(Float)
    spending_score = Column(Float)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    entered_by = Column(String(200))

    store = relationship("Store", back_populates="customers")


_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        url = get_database_url()
        if url.startswith("sqlite"):
            _engine = create_engine(url, connect_args={"check_same_thread": False})
        else:
            _engine = create_engine(
                url, pool_pre_ping=True, connect_args={"connect_timeout": 20}
            )
    return _engine


def get_sessionmaker():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _SessionLocal


@contextmanager
def session():
    s = get_sessionmaker()()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def init_db() -> None:
    Base.metadata.create_all(get_engine())


def _seed_email(name: str) -> str:
    return f"{re.sub(r'[^a-z0-9]+', '', name.lower())}@mallsegment.local"


def seed_initial_data() -> None:
    """Idempotently seed the 7 tenant stores and the 200-row demo dataset."""
    from utils.auth import hash_password, random_password
    from utils.stores import STORE_METADATA

    csv_path = _ROOT / "data" / "Mall_Customers.csv"
    with session() as s:
        if s.query(Store).count() == 0:
            for name, meta in STORE_METADATA.items():
                s.add(
                    Store(
                        name=name,
                        email=_seed_email(name),
                        category=meta["category"],
                        icon=meta["icon"],
                        color=meta["color"],
                        password_hash=hash_password(random_password()),
                        status="approved",
                        created_by="seed",
                        approved_at=datetime.now(timezone.utc),
                    )
                )
            s.flush()

        if s.query(Customer).count() == 0 and csv_path.exists():
            df = pd.read_csv(csv_path)
            name_to_id = {st.name: st.id for st in s.query(Store).all()}
            for _, r in df.iterrows():
                sid = name_to_id.get(r.get("Store Visited"))
                if sid is None:
                    continue
                s.add(
                    Customer(
                        store_id=sid,
                        gender=r.get("Gender"),
                        age=int(r["Age"]),
                        annual_income=float(r["Annual Income (k$)"]),
                        spending_score=float(r["Spending Score (1-100)"]),
                        entered_by="seed",
                    )
                )


# ── Demo store accounts ──────────────────────────────────────────────────────
# Credentials for these are safe to display on demo deployments; they exist only
# to let someone try the store experience, and hold no real customer data.
DEMO_STORES = [
    {
        "name": "Demo Store — Fashion",
        "email": "demo.fashion@mallsegment.local",
        "password": "demo1234",
        "category": "Fashion",
        "icon": "👗",
        "color": "#EC4899",
    },
    {
        "name": "Demo Store — Electronics",
        "email": "demo.electronics@mallsegment.local",
        "password": "demo1234",
        "category": "Electronics",
        "icon": "💻",
        "color": "#3B82F6",
    },
    {
        "name": "Demo Store — Grocery",
        "email": "demo.grocery@mallsegment.local",
        "password": "demo1234",
        "category": "Grocery",
        "icon": "🥬",
        "color": "#22C55E",
    },
]


def ensure_demo_stores() -> list[dict]:
    """Create any missing demo stores, each with a few sample shoppers.

    Idempotent: existing demo stores are left untouched, so records a visitor
    entered by hand survive a restart.
    """
    created = []
    for spec in DEMO_STORES:
        if get_store_by_email(spec["email"]) is not None:
            continue
        store = create_store(
            name=spec["name"],
            email=spec["email"],
            category=spec["category"],
            icon=spec["icon"],
            color=spec["color"],
            password=spec["password"],
            status="approved",
            created_by="seed",
        )
        for gender, age, income, score in (
            ("Female", 29, 62.0, 71.0),
            ("Male", 41, 88.0, 34.0),
            ("Female", 35, 45.0, 82.0),
        ):
            add_customer(
                store_id=store["id"],
                gender=gender,
                age=age,
                annual_income=income,
                spending_score=score,
                entered_by=spec["email"],
            )
        created.append(store)
    return created


# ── Store helpers ────────────────────────────────────────────────────────────
def list_stores(status: str | None = None) -> list[dict]:
    with session() as s:
        q = s.query(Store).order_by(Store.name)
        if status:
            q = q.filter(Store.status == status)
        return [
            {
                "id": st.id,
                "name": st.name,
                "email": st.email,
                "category": st.category,
                "icon": st.icon,
                "color": st.color,
                "status": st.status,
                "created_by": st.created_by,
                "created_at": st.created_at,
                "approved_at": st.approved_at,
            }
            for st in q.all()
        ]


def store_overview() -> list[dict]:
    """Every store with its live shopper count, for the admin management table."""
    with session() as s:
        rows = (
            s.query(Store, func.count(Customer.id))
            .outerjoin(Customer, Customer.store_id == Store.id)
            .group_by(Store.id)
            .order_by(Store.name)
            .all()
        )
        return [
            {
                "id": st.id,
                "name": st.name,
                "email": st.email,
                "category": st.category,
                "icon": st.icon,
                "color": st.color,
                "status": st.status,
                "created_by": st.created_by,
                "created_at": st.created_at,
                "approved_at": st.approved_at,
                "shoppers": count,
            }
            for st, count in rows
        ]


def get_store(store_id: int) -> dict | None:
    with session() as s:
        st = s.get(Store, store_id)
        if st is None:
            return None
        return {
            "id": st.id,
            "name": st.name,
            "email": st.email,
            "category": st.category,
            "icon": st.icon,
            "color": st.color,
            "status": st.status,
            "created_by": st.created_by,
        }


def get_store_by_email(email: str) -> dict | None:
    with session() as s:
        st = (
            s.query(Store)
            .filter(func.lower(Store.email) == (email or "").strip().lower())
            .first()
        )
        if st is None:
            return None
        return {
            "id": st.id,
            "name": st.name,
            "email": st.email,
            "status": st.status,
            "password_hash": st.password_hash,
        }


def get_store_by_name(name: str) -> dict | None:
    with session() as s:
        st = (
            s.query(Store)
            .filter(func.lower(Store.name) == (name or "").strip().lower())
            .first()
        )
        return None if st is None else {"id": st.id, "name": st.name, "status": st.status}


def create_store(
    name: str,
    email: str,
    category: str = "General",
    icon: str = "🛍️",
    color: str = "#7C3AED",
    password: str | None = None,
    status: str = "pending",
    created_by: str = "self",
) -> dict:
    """Create a store and return its details plus the plaintext password once."""
    from utils.auth import hash_password, random_password

    pw = password or random_password()
    with session() as s:
        row = Store(
            name=name.strip(),
            email=email.strip().lower(),
            category=category or "General",
            icon=icon or "🛍️",
            color=color or "#7C3AED",
            password_hash=hash_password(pw),
            status=status,
            created_by=created_by,
            approved_at=datetime.now(timezone.utc) if status == "approved" else None,
        )
        s.add(row)
        s.flush()
        return {"id": row.id, "name": row.name, "email": row.email, "password": pw}


def set_store_status(store_id: int, status: str) -> None:
    if status not in STORE_STATUSES:
        raise ValueError(f"Unknown store status: {status}")
    with session() as s:
        st = s.get(Store, store_id)
        if st is None:
            return
        st.status = status
        if status == "approved":
            st.approved_at = datetime.now(timezone.utc)


def reset_store_password(store_id: int) -> str | None:
    from utils.auth import hash_password, random_password

    pw = random_password()
    with session() as s:
        st = s.get(Store, store_id)
        if st is None:
            return None
        st.password_hash = hash_password(pw)
    return pw


def delete_store(store_id: int) -> bool:
    """Remove a store and (via cascade) all of its customer records."""
    with session() as s:
        st = s.get(Store, store_id)
        if st is None:
            return False
        s.query(Customer).filter(Customer.store_id == store_id).delete(
            synchronize_session=False
        )
        s.delete(st)
        return True


# ── Customer helpers ─────────────────────────────────────────────────────────
def add_customer(
    store_id: int,
    gender: str,
    age: int,
    annual_income: float,
    spending_score: float,
    entered_by: str | None = None,
) -> int:
    with session() as s:
        c = Customer(
            store_id=store_id,
            gender=gender,
            age=int(age),
            annual_income=float(annual_income),
            spending_score=float(spending_score),
            entered_by=entered_by,
        )
        s.add(c)
        s.flush()
        return c.id


def delete_customer(customer_id: int, store_id: int | None = None) -> bool:
    with session() as s:
        c = s.get(Customer, customer_id)
        if c is None:
            return False
        if store_id is not None and c.store_id != store_id:
            return False
        s.delete(c)
        return True


def load_customers_df(store_id: int | None = None) -> pd.DataFrame:
    """Return customers in the exact column shape the analytics pages expect."""
    with session() as s:
        q = s.query(Customer, Store).join(Store, Customer.store_id == Store.id)
        if store_id is not None:
            q = q.filter(Customer.store_id == store_id)
        rows = q.order_by(Customer.id).all()

    records = [
        {
            "CustomerID": c.id,
            "Gender": c.gender,
            "Age": c.age,
            "Annual Income (k$)": c.annual_income,
            "Spending Score (1-100)": c.spending_score,
            "Store Visited": st.name,
            "Store Category": st.category,
        }
        for c, st in rows
    ]
    return pd.DataFrame(records, columns=CUSTOMER_COLUMNS)
