"""
Database initialization script.
Run once: python database/init_db.py
Creates trucks.db in the database/ directory and inserts sample data.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "trucks.db")


def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trucks (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            brand               TEXT NOT NULL,
            model               TEXT NOT NULL,
            category            TEXT,
            length_m            REAL,
            width_m             REAL,
            height_m            REAL,
            max_load_ton        REAL,
            gross_weight_ton    REAL,
            engine_hp           INTEGER,
            fuel_type           TEXT,
            emission_standard   TEXT,
            target_market       TEXT,
            status              TEXT DEFAULT 'active'
        )
    """)

    sample_trucks = [
        ("Volvo",        "FH16 750",     "Heavy",  16.5, 2.50, 3.9, 25.0, 40.0, 750, "Diesel", "Euro 6",   "EU"),
        ("Volvo",        "FM 460",        "Heavy",  16.0, 2.50, 3.8, 22.0, 40.0, 460, "Diesel", "Euro 6",   "EU"),
        ("Scania",       "R 500",         "Heavy",  17.0, 2.50, 3.9, 24.0, 40.0, 500, "Diesel", "Euro 6",   "EU"),
        ("Scania",       "G 410",         "Heavy",  16.5, 2.50, 3.8, 22.0, 38.0, 410, "Diesel", "Euro 6",   "EU,CN"),
        ("MAN",          "TGX 640",       "Heavy",  17.2, 2.50, 4.0, 25.0, 40.0, 640, "Diesel", "Euro 6",   "EU"),
        ("FAW",          "J7",            "Heavy",  17.5, 2.55, 3.95,27.0, 49.0, 550, "Diesel", "China 6",  "CN"),
        ("Dongfeng",     "Tianlong",      "Heavy",  17.8, 2.55, 3.95,28.0, 49.0, 520, "Diesel", "China 6",  "CN"),
        ("Sinotruk",     "HOWO T7H",      "Heavy",  18.0, 2.55, 4.0, 30.0, 49.0, 540, "Diesel", "China 6",  "CN"),
        ("Kenworth",     "T680",          "Heavy",  19.5, 2.55, 4.1, 28.0, 36.0, 500, "Diesel", "EPA2021",  "US"),
        ("Peterbilt",    "579",           "Heavy",  20.0, 2.55, 4.0, 27.0, 36.0, 480, "Diesel", "EPA2021",  "US"),
        ("Freightliner", "Cascadia",      "Heavy",  19.8, 2.55, 4.1, 29.0, 36.0, 500, "Diesel", "EPA2021",  "US"),
        ("Mercedes",     "Actros 2663",   "Heavy",  16.8, 2.50, 3.9, 24.0, 40.0, 630, "Diesel", "Euro 6",   "EU"),
        ("FAW",          "J6P",           "Heavy",  17.2, 2.55, 3.9, 25.0, 49.0, 460, "Diesel", "China 6",  "CN"),
        ("Volvo",        "FE 280",        "Medium", 10.5, 2.40, 3.5, 12.0, 18.0, 280, "Diesel", "Euro 6",   "EU"),
        ("MAN",          "TGL 12",        "Medium", 10.0, 2.35, 3.4, 10.0, 12.0, 220, "Diesel", "Euro 6",   "EU"),
    ]

    cursor.executemany("""
        INSERT INTO trucks
            (brand, model, category, length_m, width_m, height_m,
             max_load_ton, gross_weight_ton, engine_hp, fuel_type,
             emission_standard, target_market)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_trucks)

    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")
    print(f"Inserted {len(sample_trucks)} sample truck records.")


if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        confirm = input("Database already exists. Re-initialize? (y/N): ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            exit()
        os.remove(DB_PATH)
        print("Old database deleted.")

    init_database()
