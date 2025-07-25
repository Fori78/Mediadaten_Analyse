# database.py

import os
import sqlite3
import pandas as pd
from typing import Optional

def _get_default_db_path() -> str:
    """Ermittelt den Standardspeicherpfad für die SQLite-Datenbank im outputs-Ordner."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "outputs"))
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "mediadaten.db")

def save_to_sqlite(df: pd.DataFrame, db_path: Optional[str] = None, table_name: str = "mediadaten") -> None:
    """Speichert ein DataFrame in eine SQLite-Datenbank."""
    if df.empty: 
        raise ValueError("Keine Daten zum Speichern vorhanden.")

    if db_path is None:
        db_path = _get_default_db_path()
    
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Datenbank gespeichert unter: {db_path}")
    finally: 
        conn.close()

def load_from_sqlite(db_path: Optional[str] = None, table_name: str = "mediadaten") -> pd.DataFrame:
    """Lädt ein gesamtes DataFrame aus einer SQLite-Datenbank."""
    if db_path is None:
        db_path = _get_default_db_path()
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Die Datenbankdatei wurde nicht gefunden: {db_path}")
    
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        print(f"Daten aus {table_name} geladen aus: {db_path}")
        return df
    finally:
        conn.close()
        
def run_query(query: str, db_path: Optional[str] = None) -> pd.DataFrame:
    """Führt eine SQL-Abfrage auf der SQLite-Datenbank aus und gibt ein DataFrame zurück."""
    if db_path is None:
        db_path = _get_default_db_path()
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Die Datenbankdatei wurde nicht gefunden: {db_path}")
    
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(query, conn)
        print(f"Abfrage erfolgreich ausgeführt:\n{query.strip()}")
        return df
    finally:
        conn.close()