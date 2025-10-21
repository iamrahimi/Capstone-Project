import pandas as pd
import sqlite3
import os
import re

# ====== Config ======
database_name = "./db/mlb_history.db"
csv_folder = "./tables"

conn = sqlite3.connect(database_name)

# ====== Helper: Infer SQLite types ======
def infer_sqlite_types(df):
    dtype_map = {}
    for col in df.columns:
        if pd.api.types.is_integer_dtype(df[col]):
            dtype_map[col] = "INTEGER"
        elif pd.api.types.is_float_dtype(df[col]):
            dtype_map[col] = "REAL"
        else:
            dtype_map[col] = "TEXT"
    return dtype_map

# ====== Loop through CSV files ======
for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(csv_folder, file))

        # --- Skip rows with more than 1 nulls ---
        df = df[df.isnull().sum(axis=1) < 2]

        # --- Fill remaining NaNs based on column type ---
        for col in df.columns:
            if pd.api.types.is_integer_dtype(df[col]):
                df[col] = df[col].fillna(0)
            elif pd.api.types.is_float_dtype(df[col]):
                df[col] = df[col].fillna(0.0)
            else:
                df[col] = df[col].fillna("N/A")

        # --- Safe table name ---
        table_name = re.sub(r"[^\w]+", "_", os.path.splitext(file)[0])

        # --- Infer SQLite types ---
        dtype_map = infer_sqlite_types(df)

        # --- Insert into SQLite ---
        df.to_sql(table_name, conn, if_exists="replace", index=False, dtype=dtype_map)
        print(f"Inserted {len(df)} rows into table '{table_name}'")

conn.commit()
conn.close()
print(f" All CSV files imported into '{database_name}'")
