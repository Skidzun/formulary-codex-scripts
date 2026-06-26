"""
extract_textlines.py

Extracts the transcribed text from all PAGE XML files in data/ and writes
them into a single combined plain-text file in output/.

Each document is preceded by a blank line and its imageFilename, e.g.:

    BayHStA_AS_Lit_Oe_463_338r.jpg
    haben ʒwelif ß wienner d$ gelltes purkchrechcʒ auf vnſeꝛm
    hof der da leit ʒu Töbling vnd auf dem pawngaꝛtn̅
    …

Expected layout:
    project/
    ├── data/        ← PAGE XML files live here
    ├── src/
    │   └── extract_textlines.py   ← this script
    └── output/      ← combined output is written here (created if absent)

Run from *any* working directory:
    python src/extract_textlines.py
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths – all relative to this script's location so the script works
# regardless of the current working directory.
# ---------------------------------------------------------------------------
SCRIPT_DIR  = Path(__file__).resolve().parent       # …/src/
PROJECT_DIR = SCRIPT_DIR.parent                     # …/project/
DATA_DIR    = PROJECT_DIR / "data"
OUTPUT_DIR  = PROJECT_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "GT.txt"

# PAGE XML namespace used in files produced by eScriptorium / Transkribus
PAGE_NS = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"


def parse_page(xml_path: Path) -> tuple[str, list[str]]:
    """
    Parse a single PAGE XML file.
    Returns (imageFilename, [text lines]) in document order.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Extract imageFilename from the <Page> element
    page_el = root.find(f"{{{PAGE_NS}}}Page")
    image_filename = page_el.get("imageFilename", xml_path.name) if page_el is not None else xml_path.name

    # Collect all Unicode text lines
    lines: list[str] = []
    for text_line in root.iter(f"{{{PAGE_NS}}}TextLine"):
        unicode_el = text_line.find(f"{{{PAGE_NS}}}TextEquiv/{{{PAGE_NS}}}Unicode")
        if unicode_el is not None and unicode_el.text:
            lines.append(unicode_el.text)

    return image_filename, lines


def calculate_gt(txt):
    with open(OUTPUT_FILE, 'r', encoding='utf8') as f:
        text = f.read()

    # Characters
    number_char = len(text)

    # Words
    text_tokenised = text.split()
    number_words = len(text_tokenised)

    # Lines — just split the string we already have, no second open() needed
    text_lines = text.splitlines()
    number_lines = len(text_lines)

    print(f'Number of characters: {number_char}')
    print(f'Number of words: {number_words}')
    print(f'Number of lines: {number_lines}')
    print('Calculating average values per page...')

    char_avg = number_char / 10
    words_avg = number_words / 10
    lines_avg = number_lines / 10

    print(f'Average number of characters per page: {char_avg}')
    print(f'Average number of words per page: {words_avg}')
    print(f'Average number of lines per page: {lines_avg}')
    print('Calculating average values per line...')

    char_line_avg = number_char / number_lines
    words_line_avg = number_words / number_lines

    print(f'Average number of characters per line: {char_line_avg}')
    print(f'Average number of words per line: {words_line_avg}')


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    xml_files = sorted(DATA_DIR.glob("*.xml"))
    if not xml_files:
        print(f"No XML files found in {DATA_DIR}")
        return

    blocks: list[str] = []
    for xml_path in xml_files:
        image_filename, lines = parse_page(xml_path)
        # Blank line, then filename header, then the text lines
        block = "\n" + image_filename + "\n" + "\n".join(lines)
        blocks.append(block)
        print(f"  {xml_path.name}  ({len(lines)} lines)  →  [{image_filename}]")

    OUTPUT_FILE.write_text("Formelbuch\n" + "\n".join(blocks), encoding="utf-8")
    print(f"\nDone. Combined output written to {OUTPUT_FILE.relative_to(PROJECT_DIR)}")
    print('Calculating total values...')

    calculate_gt(OUTPUT_FILE)
    print("Done.")


if __name__ == "__main__":
    main()