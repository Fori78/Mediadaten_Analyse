'''
Q-Daten (BMW & Mercedes-Benz) automatisch (auch für künftige Quartale und Marken) einlesen und zusammenführen.
In den Dateien eine neue Spalte "Brand" hinzufügen, das aus dem Dateinamen extrahiert wird.
Gruppiert Medien grob in Social Media und Online News.
In den Dateien eine neue Spalte "Quartal", "Day", "Month", Year" aus "Published" hinzufügen
    Optional: fallback für Quartal aus Dateinamen, falls kein valides Datum.
Code so vorbereiten, dass Q2/Q3 später ergänzt werden können.
EMV und Media Reach berechnen
    EMV = (engagement + 0.1 * media_reach) * sentiment_factor
    MediaReach = (Views if vorhanden else Reach) * CredibilityScore

Warum OOP hier sinnvoll ist
Mit OOP kannst du:
    den Zustand (z. B. data_dir, DataFrames) kapseln,
    verwandte Funktionen methodisch bündeln (z. B. als self.load_data() statt load_all_mediadaten(...)),
    später leichter erweitern (z. B. für weitere Analysen, Reports, Validierungen),
    mehr Wiederverwendbarkeit und Testbarkeit erreichen.

Wir bauen eine Klasse MediaDataProcessor, die alles rund um Laden, Verarbeiten und Berechnen kapselt.
'''

# analyse.py

import pandas as pd
import os
import glob
import re
from mediadaten_analyse.analyse.config_loader import load_credibility_scores
import sqlite3

class MediaDataProcessor:
    sentiment_map = {
        "positiv": 1.0,
        "neutral": 0.7,
        "negativ": -1.0
    }

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.df = pd.DataFrame()
        self.credibility_scores = {}

    def load(self):
        self.df = self._load_all_mediadaten()
        self.credibility_scores = load_credibility_scores(
            os.path.join(self.data_dir, "credibility_scores.xlsx")
        )
        self._calculate_metrics()
        return self.df
    
    # Lädt und merged alle mediadaten_*.xlsx-Dateien aus dem angegebenen Verzeichnis.
    # Ergänzt automatisch Brand, Datumskomponenten & Quartal.
    def _load_all_mediadaten(self):
        pattern = os.path.join(self.data_dir, "[Mm]ediadaten_*.xlsx")
        file_paths = glob.glob(pattern)

        if not file_paths:
            raise FileNotFoundError("Keine passenden Dateien gefunden.")

        dfs = []
        for path in file_paths:
            brand = self._extract_brand_from_filename(path)
            df = pd.read_excel(path)
            if df.empty:
                continue

            df["Brand"] = brand
            df["Published"] = pd.to_datetime(df["Published"], errors="coerce")
            df["Year"] = df["Published"].dt.year
            df["Month"] = df["Published"].dt.month
            df["Day"] = df["Published"].dt.day
            df["Quartal"] = (
                "Q" + ((df["Month"] - 1) // 3 + 1).astype(str) + "_" + df["Year"].astype(str)
            )
            '''
            df["Month"] enthält die Monatszahl aus dem Datum, z. B. 1 für Januar.
            "Q" + ... : Baut den Quartals-String auf, z. B. "Q1"
            (df["Month"] - 1) // 3: Quartalsberechnung
            +1 Echte Quratale erhalten: Q1.
            .astype(str) wandelt die Quartalszahl (1, 2, …) in einen String um, 
                damit sie in Text verkettet werden kann.
            + "_" + df["Year"].astype(str): Hängt noch das Jahr dran, also "Q1_2025"
            '''

            dfs.append(df)

        return pd.concat(dfs, ignore_index=True)
            
    # In den Dateien eine neue Spalte "Brand" hinzufügen, das aus dem Dateinamen extrahiert wird.
    def _extract_brand_from_filename(self, filename):
        name = os.path.splitext(os.path.basename(filename))[0]
        match = re.match(r"mediadaten_(.+?)_Q\d{1,2}_\d{4}", name)
        return match.group(1) if match else "Unbekannt"

    def _get_sentiment_factor(self, sentiment):
        return self.sentiment_map.get(str(sentiment).lower(), 0.7)
    
    '''
    Berechnungen: EMV, Media Reach
    '''
    def _calculate_metrics(self):
        self.df["Media Reach"] = self.df.apply(self._calculate_media_reach, axis=1)
        self.df["EMV"] = self.df.apply(self._calculate_emv, axis=1)
        self.df["Media Branch"] = self.df["Medium"].apply(self._map_media_branch)
    
    def _map_media_branch(self, medium):
        """
        Gruppiert Medien grob in Social Media und Online News.
        Alles, was nicht als Social Media erkannt wird, fällt automatisch unter Online News.
        """
        medium = str(medium).lower()
        if any(x in medium for x in ["x", "twitter", "facebook", "instagram", "linkedin", "tiktok", "youtube"]):
           return "Social Media"
        else:
           return "Online News"
    
    def _calculate_media_reach(self, row):
        value = row.get("Views") if pd.notna(row.get("Views")) else row.get("Reach")
        medium = str(row.get("Medium")).lower()
        credibility = self.credibility_scores.get(medium, 1)
        return value * credibility if pd.notna(value) else 0

    def _calculate_emv(self, row):
        likes = row.get("Likes") or 0
        shares = row.get("Shares") or 0
        comments = row.get("Comments") or 0
        engagement = likes + shares + comments

        sentiment_factor = self._get_sentiment_factor(row.get("Sentiment"))
        media_reach = row.get("Media Reach") or 0
        return (engagement + 0.1 * media_reach) * sentiment_factor

        
        



"""
Funktionalität	             OOP (neu)
Wiederverwendbarkeit	     Hoch
Erweiterbarkeit	             mit Klassenvererbung möglich
Testbarkeit	                 Methoden einzeln testbar
Lesbarkeit	                 klar strukturierte Objekte
Zustand behalten	         automatisch über self
"""