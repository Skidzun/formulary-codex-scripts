'''
Dieses Skript ermöglicht es, automatisiert Überschriften der Formulare
zu extrahieren.

Das Skript setzt folgende Ordnerstruktur voraus:
Parent  / src (hier liegt das Skript)
        / data (hier liegen die PAGE xml-Dateien)
        / output (für die CSV-Daten, wird ggf. automatisch erstellt)

Input: PAGE xml-Dateien mit Transkriptionen
Output: CSV-Datei mit Folionummern, Formularüberschriften
'''

from pathlib import Path
import csv
import xml.etree.ElementTree as ET
import re

# Pfade definieren
SRC_DIR = Path(__file__).resolve().parent # Ordner mit diesem Skript
DATA_DIR = SRC_DIR.parent / "data" # Ordner mit den Eingabedaten (PAGE xml)
OUTPUT_CSV = SRC_DIR.parent / "output" / "header_lines.csv" # Ausgabe der CSV
CLEANED_CSV = SRC_DIR.parent / "output" / "header_lines_cleaned.csv" # Ausgabe der bereinigten CSV

# PAGE XML namespace definieren
NS = {
    "page": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"
}

def extract_header_lines(xml_file):
    """
    Funktion, die alle header lines mit der Value:
    custom="structure {type:header line;}"
    extrahiert
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    results = []

    for textline in root.findall(".//page:TextLine", NS):

        custom = textline.attrib.get("custom", "")

        # Alle Textzeilen mit der value "header line" finden
        if custom == "structure {type:header line;}":

            unicode_el = textline.find(".//page:Unicode", NS)

            if unicode_el is not None and unicode_el.text:
                results.append(unicode_el.text.strip())

    return results

def clean_csv(input_csv, output_csv):

    '''
    Funktion, um aus den in Spalte 1 gespeichrten Dateinamen
    der PAGE xmls die Folionummerierung zu generieren.
    '''

    # Ruft die Output-Datei auf und erstellt eine bereinigte Datei
    with open(OUTPUT_CSV, "r", encoding="utf-8") as infile, \
        open(CLEANED_CSV, "w", encoding="utf-8") as outfile:

        # Spaltenüberschriften bewahren
        header = infile.readline()
        outfile.write(header)

        # Alle anderen Zeilen der ersten Spalte ansteuern
        for line in infile:

            # Zeilen aufheben
            line = line.rstrip("\n")

            # Zeilen am ersten Komma trennen
            parts = line.split(",", 1)

            # Erste Spalte ansteuern
            filename = parts[0]

            # Zahlen aus erster Spalte extrahieren
            number_groups = re.findall(r'\d+[rv]?', filename)

            # Die erste Zahl (463) entfernen
            if len(number_groups) > 1:
             remaining_number = ''.join(number_groups[1:])
            else:
                remaining_number = ""

            # Zeilen neu zusammensetzen
            if len(parts) > 1:
                new_line = remaining_number + "," + parts[1]
            else:
                new_line = remaining_number

            outfile.write(new_line + "\n")

def main():
    '''
    Hauptfunktion, welche die Daten extrahiert
    und als csv zurückgibt
    '''

    # XML files suchen
    xml_files = sorted(DATA_DIR.glob("*.xml"))

    if not xml_files:
        print(f"No XML files found in: {DATA_DIR}")
        return

    rows = []

    # Formularüberschriften extrahieren
    for xml_file in xml_files:

        headers = extract_header_lines(xml_file)

        if headers:
            for header in headers:
                rows.append({
                    "folium": xml_file.name,
                    "header": header
                })
        else:
            rows.append({
                "folium": xml_file.name,
                "header": ""
            })

    # Prüfen, ob Output-Ordner vorhanden ist:
    # Wenn nicht wird Ordner erstellt.
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    
    # CSV schreiben
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:

        # Definiert die Spalten-Header
        writer = csv.DictWriter(
            csvfile,
            fieldnames=["folium", "header", "type"]
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} rows to:")
    print(OUTPUT_CSV)

    clean_csv(OUTPUT_CSV, CLEANED_CSV)

    print("Finished generating folio numbers.")

# Hauptfunktion aufrufen (startet den zuvor definierten Ablauf)
if __name__ == "__main__":
    main()