# query_tool.py

import sys
import os
import argparse
import pandas as pd
from mediadaten_analyse.analyse.database import run_query

# Projektpfad einbinden
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Output-Verzeichnis vorbereiten
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "outputs"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_to_excel(df: pd.DataFrame, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    df.to_excel(path, index=False)
    print(f"Ergebnis gespeichert unter: {path}")

def get_filtered_posts(brand=None, quarter=None, sentiment=None, min_reach=None,
                       media_branch=None, ceo=None, engagement=None,
                       medium=None, country=None) -> pd.DataFrame:
    conditions = []

    if brand:
        conditions.append(f"LOWER(Brand) LIKE LOWER('%{brand}%')")
    if quarter:
        conditions.append(f"Quartal = '{quarter}'")
    if sentiment:
        conditions.append(f"Sentiment = '{sentiment}'")
    if min_reach:
        conditions.append(f"[Media Reach] > {min_reach}")
    if media_branch:
        conditions.append(f"LOWER([Media Branch]) LIKE LOWER('%{media_branch}%')")
    if ceo:
        conditions.append(f"LOWER(CEO) LIKE LOWER('%{ceo}%')")
    if engagement:
        conditions.append(f"Engagement > {engagement}")
    if medium:
        conditions.append(f"LOWER(Medium) LIKE LOWER('%{medium}%')")
    if country:
        conditions.append(f"LOWER(Country) LIKE LOWER('%{country}%')")

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT * FROM mediadaten
        WHERE {where_clause}
    """
    df = run_query(query)

    filename_parts = ["filtered"]
    for val in [brand, quarter, sentiment, min_reach, media_branch, ceo, engagement, medium, country]:
        if val:
            filename_parts.append(str(val).replace(" ", "_"))
    
    filename = "_".join(filename_parts) + ".xlsx"
    save_to_excel(df, filename)
    return df

def get_emv_trend_for_brand(brand: str) -> pd.DataFrame:
    query = f"""
        SELECT Quartal, SUM(EMV) AS Gesamt_EMV
        FROM mediadaten
        WHERE Brand = '{brand}'
        GROUP BY Quartal
        ORDER BY Quartal
    """
    df = run_query(query)
    save_to_excel(df, f"emv_trend_{brand}.xlsx")
    return df

# Hauptprogramm
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Datenbankabfragen auf mediadaten.db")

    parser.add_argument("--mode", type=str, required=True, choices=["filtered", "emv_trend", "negative_posts"],
                        help="Modus der Abfrage: filtered, emv_trend, negative_posts")
    parser.add_argument("--brand", type=str, help="Marke, z. B. 'BMW'")
    parser.add_argument("--quarter", type=str, help="Quartal, z. B. 'Q2_2025'")
    parser.add_argument("--sentiment", type=str, help="Sentiment: positiv, neutral, negativ")
    parser.add_argument("--min-reach", type=int, help="Minimale Media Reach")
    parser.add_argument("--media-branch", type=str, help="Medienbranche")
    parser.add_argument("--ceo", type=str, help="CEO-Name")
    parser.add_argument("--engagement", type=float, help="Mindest-Engagement")
    parser.add_argument("--medium", type=str, help="Medium")
    parser.add_argument("--country", type=str, help="Land")

    args = parser.parse_args()

    if args.mode == "filtered":
        get_filtered_posts(
            brand=args.brand,
            quarter=args.quarter,
            sentiment=args.sentiment,
            min_reach=args.min_reach,
            media_branch=args.media_branch,
            ceo=args.ceo,
            engagement=args.engagement,
            medium=args.medium,
            country=args.country
        )
    elif args.mode == "emv_trend":
        if not args.brand:
            parser.error("--brand ist erforderlich für Modus 'emv_trend'")
        get_emv_trend_for_brand(args.brand)
    elif args.mode == "negative_posts":
        if not args.brand or not args.quarter:
            parser.error("--brand und --quarter sind erforderlich für Modus 'negative_posts'")
        get_filtered_posts(
            brand=args.brand,
            quarter=args.quarter,
            sentiment="negativ"
        )




# Beispielaufrufe im Terminal

# Im richtigen Ordner:
# cd C:\Users\Hykki\verzeichnis\Mediadaten_Analyse
# set PYTHONPATH=.

# Für negative Posts
# python mediadaten_analyse\tools\query_tool.py --brand BMW --quarter Q1_2025 --mode negative_posts

# Für EMV-Trend
# python mediadaten_analyse\tools\query_tool.py --brand BrandX --mode emv_trend

# Nur BMW, Quartal Q2_2025, Sentiment negativ
# python mediadaten_analyse\tools\query_tool.py --mode filtered --brand BMW --quarter Q2_2025 --sentiment negativ

# Filter mit Mindestreichweite
# python mediadaten_analyse\tools\query_tool.py --mode filtered --brand BMW --min-reach 20000

# EMV-Trend
# python mediadaten_analyse\tools\query_tool.py --mode emv_trend --brand BMW

# Klassisch: negative Posts
# python mediadaten_analyse\tools\query_tool.py --mode negative_posts --brand BMW --quarter Q2_2025

# Nur nach Marke filtern
# python mediadaten_analyse/tools/query_tool.py --mode filtered --brand BMW

# Nach Marke, CEO und Land
# python mediadaten_analyse/tools/query_tool.py --mode filtered --brand BMW --ceo "Oliver Zipse" --country Germany

# Alle negativen Beiträge von Tesla im Q2
# python mediadaten_analyse/tools/query_tool.py --mode filtered --brand Tesla --quarter Q2_2025 --sentiment negativ

# Hohe Reichweite & Engagement in der Automobilbranche
# python mediadaten_analyse/tools/query_tool.py --mode filtered --media-branch "Automotive" --min-reach 50000 --engagement 0.05

# Nach Medium und Land
# python mediadaten_analyse/tools/query_tool.py --mode filtered --medium "YouTube" --country USA
            