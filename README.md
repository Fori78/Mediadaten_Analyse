# README.md

# Mediadaten Analyse

Dieses Projekt ist mein erstes Projekt in Python und dient sowohl Lern- als auch Analysezwecken.
Ein Analyse-, Filterung- und Visualisierungstool für Mediadaten, 
z. B. zur Bewertung von Marken oder CEOs mit Credibility Scoring.

## Features

- Datenimport und -verarbeitung
- Automatische Datenzusammenführung (Merge)
- Credibility Scoring (konfigurierbar)
- Filterung nach Marke, Quartal, Sentiment, Reichweite u.v.m.
- EMV-Trend-Analyse
- Sentiment-Auswertung (positiv, neutral, negativ)
- Visualisierung von Mediadaten (Media Reach, Sentiment, Branchenverteilung)
- Export als Excel-Dateiund SQLite-Datenbank
- CLI-Unterstützung mit Argumenten

## Nutzung

# Start mit Standarddaten
python -m mediadaten_analyse

# Query Tool – Beispiel:
python mediadaten_analyse/tools/query_tool.py --mode filtered --brand BMW --quarter Q2_2025

# Nur negative Posts von Tesla im Q2 2025:
python mediadaten_analyse/tools/query_tool.py --mode filtered --brand Tesla --quarter Q2_2025 --sentiment negativ

# EMV-Trend für BMW
python mediadaten_analyse/tools/query_tool.py --mode emv_trend --brand BMW


## Installation

git clone https://github.com/dein-nutzername/mediadaten-analyse.git
cd mediadaten-analyse
pip install .

## Virtuelle Umgebung
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

## Abhängigkeiten installieren
pip install -r requirements.txt


## Projektstruktur
mediadaten_analyse/
├── analyse/ # Datenverarbeitung, Analyse-Logik, SQLite-Datenbank
├── tools/ # Query Tool zur gezielten Abfrage
├── visualisierung/ # Visualisierung der Ergebnisse
├── data/ # Eingangsdaten (z. B. CSV/Excel-Dateien)
├── outputs/ # Ergebnisse (Excel-Dateien, Visualisierungen)

## Autor
Hristofor Hrisoskulov
📧 h.hrisoskulov@arcor.de



```bash
git add README.md
git commit -m "README hinzugefügt"
git push
