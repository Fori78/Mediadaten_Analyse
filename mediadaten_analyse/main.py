# main.py 

import argparse
import os
import sys

# Set working directory to the script location
current_dir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(current_dir)

# Add project root to sys.path
# sys.path.insert(0, current_dir)

# Eigene Module importieren
from mediadaten_analyse.analyse.analyse import MediaDataProcessor
from mediadaten_analyse.analyse.config_loader import load_credibility_scores
from mediadaten_analyse.visualisierung.visualizer import Visualizer
from mediadaten_analyse.analyse.database import save_to_sqlite


class MainApp:
    def __init__(self, data_dir, analyse_dimension="Brand"):
        self.data_dir = data_dir
        self.analyse_dimension = analyse_dimension
        self.df = None

    def load_and_process(self):
        processor = MediaDataProcessor(self.data_dir)
        self.df = processor.load()

    def export_data(self, filename="merged_mediadaten_FINAL_EXPORT.xlsx"):
        if self.df is None:
            raise RuntimeError("Daten wurden noch nicht geladen.")
        output_path = os.path.join(self.data_dir, filename)
        self.df.to_excel(output_path, index=False)
        print(f"Exportiert nach: {output_path}")

    def visualize(self):
        if self.df is None:
            raise RuntimeError("Daten wurden noch nicht geladen.")
        viz = Visualizer(self.df)
        viz.plot_monthly_media_reach(analyse_dimension=self.analyse_dimension)

    def show_sentiment(self, analyse_dimension=None):
        viz = Visualizer(self.df)
        dim = analyse_dimension if analyse_dimension is not None else self.analyse_dimension
        viz.plot_sentiment_piecharts(analyse_dimension=dim)
        
    def show_media_branch_distribution(self):
        viz = Visualizer(self.df)
        viz.plot_media_branch_distribution()
    
    def save_to_sqlite(self, db_path="mediadaten.db"):
        if self.df is None:
            raise ValueError("Keine Daten vorhanden.")
        save_to_sqlite(self.df, db_path=db_path)
    
    def run(self, export=True, show_plot=True):
        self.load_and_process()
        self.save_to_sqlite()
        if export:
            self.export_data()
        if show_plot:
            self.visualize()
            self.show_sentiment(analyse_dimension="Brand")
            self.show_sentiment(analyse_dimension="CEO")
            self.show_media_branch_distribution()


def main():
    parser = argparse.ArgumentParser(description="Mediadaten Analyse Tool")
    parser.add_argument(
        "--dimension",
        type=str,
        default="Brand",
        help="Analyse-Dimension (z. B. Brand, CEO, Media Branch)"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data")),
        help="Pfad zum Datenordner (default: ../data)"
    )
    parser.add_argument(
        "--no-export",
        action="store_true",
        help="Deaktiviere den Datenexport"
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Deaktiviere das Anzeigen von Visualisierungen"
    )

    args = parser.parse_args()

    app = MainApp(
        data_dir=args.data_dir,
        analyse_dimension=args.dimension
    )
    app.run(
        export=not args.no_export,
        show_plot=not args.no_plot
    )
    # print(f"Analyse gestartet mit Dimension: {args.dimension}")
    # print(f"Datendirectory: {args.data_dir}")


if __name__ == "__main__":
    main()
    

# Beispielaufrufe im Terminal:

# Starten im Projektverzeichnis
    # cd "C:\Users\Hykki\verzeichnis\Mediadaten_Analyse" - Beispielordner
    
# Standard (wie vorher)
# python -m mediadaten_analyse

# Mit CEO-Analyse
# python -m mediadaten_analyse --dimension CEO

# Nur laden, kein Plot, kein Export
# python -m mediadaten_analyse --no-export --no-plot

# Mit anderem Datenverzeichnis
# python -m mediadaten_analyse --data-dir "C:/Users/Hykki/Dokumente/andere_daten"

