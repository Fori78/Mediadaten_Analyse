# setup.py

from setuptools import setup, find_packages

setup(
    name='mediadaten_analyse',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "pandas", "matplotlib", "numpy", "openpyxl"  # was eben gebraucht ist
    ],
    author="Hristofor Hrisoskulov",
    description="Analyse und Visualisierung von Mediadaten mit Credibility Scoring.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
       'console_scripts': [
        'mediadaten-analyse=mediadaten_analyse.main:main',
        'mediadaten-query=mediadaten_analyse.tools.query_tool:main'
    ]
    },
)
