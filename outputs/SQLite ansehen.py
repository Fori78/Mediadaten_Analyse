# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 13:49:33 2025

@author: Hykki
"""
# SQLite ansehen.py

import sqlite3
import pandas as pd

conn = sqlite3.connect("mediadaten.db")
df = pd.read_sql_query("SELECT * FROM mediadaten", conn)
conn.close()

print(df.head())  # oder df.columns, df.describe() etc.

# from mediadaten_analyse.analyse.database import load_from_sqlite, run_query

# # Alles laden
# df = load_from_sqlite()

# # Eine benutzerdefinierte SQL-Abfrage
# df_filtered = run_query("SELECT Brand, EMV FROM mediadaten WHERE Sentiment = 'positiv'")
# print(df_filtered.head())


from mediadaten_analyse.analyse.database import load_from_sqlite

df = load_from_sqlite()
print(df.columns)
print(df[df["Brand"] == "Mercedes-Benz"]["Quartal"].value_counts())
print(df[df["Brand"] == "Mercedes-Benz"]["Sentiment"].value_counts())

# wie dein Brand in der Datenbank genau gespeichert ist
from mediadaten_analyse.analyse.database import load_from_sqlite

df = load_from_sqlite()
print(df["Brand"].unique())


