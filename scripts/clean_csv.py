import csv
import re

def clean_text(txt):
    '''
    Function to clean various elements inserted
    during the output from eScriptorium.
    '''
    txt = txt.replace("&#x27;","'")
    txt = txt.replace("&quot;","\"")
    txt = txt.replace("⁄","/")

    txt = re.sub(r"Element 1 \(BayHStA_AS_Lit_Oe_463_|\.jpg\)", "", txt)
    txt = re.sub(r"(\d+v)", r"Folio \1", txt)

    return txt

def normalise_text(txt):
    '''
    Function to normalise various aspects of
    a transcribed text.
    '''
    replacements = {
        "ꝛt'":"etc.",
        "ij":"ii",
        "ſ":"s",
        "ꝛ":"r",
        "Ʒ":"Z",
        "ʒ":"z",
        "ů":"u",
        "ü":"u",
        "ú":"u",
        "ó":"o",
        "ö":"o",
        "ò":"o",
        "á":"a",
        "ä":"a",
        "é":"e",
        "#":"[...]"
    }

    txt = txt.lower()

    for old, new in replacements.items():
        txt = txt.replace(old,new)

    return txt

input_csv = "../data/header_lines_cleaned100.csv"
output_csv = "../output/header_lines_cleaned100.csv"

with open(input_csv, "r", encoding="utf-8") as infile, \
     open(output_csv, "w", encoding="utf-8") as outfile:

    for line in infile:

        # Remove newline temporarily
        line = line.rstrip("\n")

        # Split only at first comma
        parts = line.split(",", 1)

        # First column = filename
        filename = parts[0]

        # Extract all number groups
        # Example:
        # BayHStA_AS_Lit_Oe_463_299v.xml
        # -> ['463', '299v']
        number_groups = re.findall(r'\d+[rv]?', filename)

        # Remove the first number (463)
        if len(number_groups) > 1:
            remaining_number = ''.join(number_groups[1:])
        else:
            remaining_number = ""

        # Rebuild row
        if len(parts) > 1:
            new_line = remaining_number + "," + parts[1]
        else:
            new_line = remaining_number

        outfile.write(new_line + "\n")

print("Finished processing all rows.")