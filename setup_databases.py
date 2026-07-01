# setup_databases.py
# This script downloads the 3 HuggingFace datasets and converts them into SQLite databases.
# You only need to run this ONCE. After that, the .db files sit in the data/ folder forever.

import sqlite3
import pandas as pd
from datasets import load_dataset
import os

# ─────────────────────────────────────────────
# WHAT IS HAPPENING HERE?
# 1. We download each dataset from HuggingFace
# 2. We convert it into a pandas DataFrame (like an Excel table in Python)
# 3. We save that DataFrame into a SQLite .db file
# 4. SQLite creates a proper table with columns and rows
# ─────────────────────────────────────────────

DATA_DIR = "data"  # folder where .db files will be saved

def clean_column_names(df):
    """
    Makes column names safe for SQL:
    - lowercase everything
    - replace spaces with underscores
    - remove special characters
    Example: "Hospital Name" → "hospital_name"
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace(r"[^\w]", "_", regex=True)
    )
    return df


def save_to_sqlite(df, db_name, table_name):
    """
    Saves a pandas DataFrame into a SQLite database file.
    - db_name   : filename like 'hospitals.db'
    - table_name: the SQL table name like 'hospitals'
    """
    db_path = os.path.join(DATA_DIR, db_name)
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"  ✅ Saved {len(df)} rows to {db_path} → table: '{table_name}'")


def setup_institutions():
    print("\n📚 Downloading Institutions dataset...")
    dataset = load_dataset("Mahadih534/Institutional-Information-of-Bangladesh", split="train")
    df = dataset.to_pandas()
    df = clean_column_names(df)
    print(f"  Columns: {list(df.columns)}")
    print(f"  Shape: {df.shape}")
    save_to_sqlite(df, "institutions.db", "institutions")


def setup_hospitals():
    print("\n🏥 Downloading Hospitals dataset...")
    dataset = load_dataset("Mahadih534/all-bangladeshi-hospitals", split="train")
    df = dataset.to_pandas()
    df = clean_column_names(df)
    print(f"  Columns: {list(df.columns)}")
    print(f"  Shape: {df.shape}")
    save_to_sqlite(df, "hospitals.db", "hospitals")


def setup_restaurants():
    print("\n🍽️  Downloading Restaurants dataset...")
    dataset = load_dataset("Mahadih534/Bangladeshi-Restaurant-Data", split="train")
    df = dataset.to_pandas()
    df = clean_column_names(df)
    print(f"  Columns: {list(df.columns)}")
    print(f"  Shape: {df.shape}")
    save_to_sqlite(df, "restaurants.db", "restaurants")


if __name__ == "__main__":
    print("=" * 50)
    print("  Bangladesh Agent — Database Setup")
    print("=" * 50)

    os.makedirs(DATA_DIR, exist_ok=True)

    setup_institutions()
    setup_hospitals()
    setup_restaurants()

    print("\n" + "=" * 50)
    print("  ✅ All 3 databases created successfully!")
    print("  📁 Check your data/ folder")
    print("=" * 50)