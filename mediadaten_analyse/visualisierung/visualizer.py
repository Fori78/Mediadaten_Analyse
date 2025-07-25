# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 15:45:58 2025

@author: Hykki
"""

# visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import calendar
import numpy as np

class Visualizer:
    def __init__(self, df):
        self.df = df.copy()
        self.df["published"] = pd.to_datetime(self.df["Published"], errors="coerce")
        self.farben_media_branch = {
            "Social Media": "#1DA1F2",  # Blau
            "Online News": "#FF9800",  # Orange
            "Other": "#9E9E9E"         # Grau
            }
        
    def plot_monthly_media_reach(self, analyse_dimension="Brand"):
        # "Brand" kann hier durch "CEO" ersetzt werden, um per CEO zu berechnen
        # Sicherstellen, dass Dimension vorhanden ist
        if analyse_dimension not in self.df.columns:
            raise ValueError(f"Analyse-Dimension '{analyse_dimension}' nicht im DataFrame gefunden.")

        # Quartal & Jahr extrahieren
        self.df["Quartal_Nr"] = self.df["Quartal"].str.extract(r"Q(\d)_\d+").astype(float)
        self.df["Quartal_Jahr"] = self.df["Quartal"].str.extract(r"Q\d_(\d+)").astype(int)
        latest = self.df.sort_values(["Quartal_Jahr", "Quartal_Nr"], ascending=False).iloc[0]
        q_num = int(latest["Quartal_Nr"])
        q_year = int(latest["Quartal_Jahr"])

        # Daten für das Jahr filtern
        df_q = self.df[self.df["published"].dt.year == q_year].copy()
        df_q["Monat"] = df_q["published"].dt.month

        # Gruppieren & Pivotieren
        grouped = df_q.groupby(["Monat", analyse_dimension])["Media Reach"].sum().reset_index()
        pivot_df = grouped.pivot(index="Monat", columns=analyse_dimension, values="Media Reach").fillna(0)

        monate = pivot_df.index.tolist()
        dimension_werte = pivot_df.columns.tolist()
        x = np.arange(len(monate))
        bar_width = 0.25

        # Farben definieren
        farben = {
            "BMW": "#0166b1",
            "Mercedes-Benz": "#37424a",
            "Audi": "#f70023",
            "Oliver Zipse": "#0166b1",
            "Ola Källenius": "#37424a",
            "Gernot Döllner": "#f70023"
        }

        # Plot vorbereiten
        fig, ax = plt.subplots(figsize=(16, 8))

        for i, wert in enumerate(dimension_werte):
            values = pivot_df[wert].values
            offset = (i - len(dimension_werte) / 2) * bar_width + bar_width / 2
            ax.bar(x + offset, values, width=bar_width, label=wert, color=farben.get(wert, "#333333"))

        # X-Achse
        ax.set_xticks(x)
        ax.set_xticklabels([calendar.month_abbr[m] for m in monate])

        # Titel & Beschriftung
        ax.set_xlabel("Month")
        ax.set_ylabel("Media Reach / in millions")
        ax.set_title(f"Monthly Media Reach per {analyse_dimension} (Q{q_num} {q_year})")

        # Y-Achse
        max_y = pivot_df.max().max()
        ax.set_ylim(0, max_y * 1.3)

        # Aktuelles Quartal farblich markieren
        quartals_monate = list(range(3 * (q_num - 1) + 1, 3 * q_num + 1))
        monat_to_idx = {monat: idx for idx, monat in enumerate(monate)}
        quartal_idxs = [monat_to_idx[m] for m in quartals_monate if m in monat_to_idx]

        if quartal_idxs:
            start = min(quartal_idxs) - 0.4
            end = max(quartal_idxs) + 0.4
            ax.axvspan(start, end, color="#59ea8c", alpha=0.1)

        # Optik
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(False)

        ax.legend(title=analyse_dimension)
        plt.tight_layout()
        plt.show()
    
    def plot_sentiment_piecharts(self, analyse_dimension="Brand"):
        if analyse_dimension not in self.df.columns:
            raise ValueError(f"Analyse-Dimension '{analyse_dimension}' nicht im DataFrame.")
        if "Sentiment" not in self.df.columns:
            raise ValueError("Spalte 'Sentiment' fehlt in den Daten")
        if "Media Reach" not in self.df.columns:
            raise ValueError("Spalte 'Media Reach' fehlt in den Daten")
        
        # Sentiment vereinheitlichen
        self.df["Sentiment"] = self.df["Sentiment"].str.capitalize().fillna("Neutral")
        
        # Farben definieren
        farben = {
            "Positiv": "#4CAF50",  # grün
            "Neutral": "#BDBDBD",  # grau
            "Negativ": "#F44336"   # rot
            }
        gruppiert = self.df.groupby([analyse_dimension, "Sentiment"])["Media Reach"].sum().reset_index()
        
        # Alle Werte für Dimensionen holen
        dimension_werte = gruppiert[analyse_dimension].unique()
        
        # Für jede Brand oder CEO ein Pie-Chart
        for wert in dimension_werte:
            df_sub = gruppiert[gruppiert[analyse_dimension] == wert]
            labels = df_sub["Sentiment"]
            sizes = df_sub["Media Reach"]
            colors = [farben.get(s, "#999999") for s in labels]
            
            # Prozentual berechnen
            total = sizes.sum()
            percent_labels = [f"{l} ({s / total:.1%})" for l, s in zip(labels, sizes)]
            
            plt.figure(figsize=(6, 6))
            plt.pie(sizes, labels=percent_labels, colors=colors, autopct="", startangle=140)
            plt.title(f"Sentiment Distribution per {analyse_dimension}: {wert}")
            plt.axis("equal")
            plt.tight_layout()
            plt.show()
    
    def plot_media_branch_distribution(self):
        if "Media Branch" not in self.df.columns:
            raise ValueError("Spalte 'Media Branch' fehlt in den Daten.")
        
        # Optional: fehlende Werte entfernen
        # self.df = self.df.dropna(subset=["Media Branch", "Media Reach"])

        # Optional: Warnung bei non-numerischen Werten
        # if not np.issubdtype(self.df["Media Reach"].dtype, np.number):
            # print("Warnung: 'Media Reach' enthält nicht-numerische Werte – wird konvertiert.")
        
        # Konvertieren, um sicherzugehen, dass Media Reach numerisch ist
        self.df["Media Reach"] = pd.to_numeric(self.df["Media Reach"], errors="coerce")
        
        farben = self.farben_media_branch
        grouped = self.df.groupby("Media Branch")["Media Reach"].sum().reset_index()
        labels = grouped["Media Branch"]
        sizes = grouped["Media Reach"]
        colors = [farben.get(branch, "#CCCCCC") for branch in labels]
        
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
        plt.title("Media Reach Distribution per Media Branch")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()