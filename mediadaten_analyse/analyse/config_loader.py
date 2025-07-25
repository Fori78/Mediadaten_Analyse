import os
import pandas as pd
import json
import sqlite3


def load_credibility_scores(path):
    """
    Lädt die Credibility Scores aus verschiedenen Formaten:
    - .xlsx  → Excel
    - .csv   → CSV-Datei
    - .json  → JSON
    - .db    → SQLite (Tabelle: credibility_scores mit Spalten Medium & Score)
    Gibt ein dict {medium_name: score}.
    Einfach austauschbar oder erweiterbar ohne Codeänderungen
    """
    
    if not os.path.exists(path): 
        raise FileNotFoundError(f"Datei nicht gefunden: {path}")
    
    ext = os.path.splitext(path)[1].lower()
    
          
    if ext == ".xlsx":
        df = pd.read_excel(path)
    elif ext == ".csv":
        df = pd.read_csv(path)
    elif ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {k.lower(): v for k, v in data.items()}
    elif ext == ".db":
        conn = sqlite3.connect(path)
        df = pd.read_sql_query("SELECT Medium, Score FROM credibility_scores", conn)
        conn.close()
    else:
        raise ValueError(f"nicht unterstütztes Format: {ext}")
    
    # Gemeinsame Verarbeitung für Excel/CSV/DB
    if "Medium" not in df.columns or "Score" not in df.columns:
        raise ValueError("Die Datei muss die Spalten 'Medium' und 'Score' enthalten.")
    
    return dict(zip(df["Medium"].str.lower(), df["Score"]))
    
      
    
    