"""
Normalise Early New High German charter transcriptions

Author: Frederik Skidzun, Berlin-Brandenburgische Akademie der Wissenschaften
fskidzun@bbaw.de

This script collects an xml file containing a diplomatic ATR ground truth
of an ENGH charter text from a source directory and normalises the ground truth
transcription. The file containing the normalised transcription is then saved 
into a seperate directory while retaining the original file name.

The character specifications follow the requirements within the project
"Regesta of Emperor Frederik III" of the Regesta Imperii. It is advisable to
adjust them to individual needs when re-using this script.

"""

from pathlib import Path

root_dir = Path("PATH") # adjust path
src_dir = root_dir/"gt_diplomatic" 
dest_dir = root_dir/"gt_extended"
file_name = "NAME" # insert file path
xml_file = src_dir/file_name

src_dir.mkdir(parents=True, exist_ok=True)
dest_dir.mkdir(parents=True, exist_ok=True)

with open (xml_file, "r", encoding="utf8") as f:
        text=f.read()

# text = text.lower() # if required uncomment this line to normalise all characters to lower case
text = text.replace("&#x27;", "'") # fixes a problem with the apostrophe when exporting xml files from eScriptorium
text = text.replace("&quot;", "\"") # fixes a problem with quotation marks when exporting xml files from eScriptorium
text = text.replace("ꝛt'", "etc.") # normalises <ꝛt'> to <etc.>
text = text.replace("ij", "ii") # normalises Latin numerals
text = text.replace("t̅ d", "Pfd. Pf.") # normalises diplomatic currency abbreviature

for c in text:
        if c in "ſ":
                text = text.replace(c, "s") # replaces all instances of <tall s> with <s>
        elif c in "ꝛ":
                text = text.replace(c, "r") # replaces all instances of r rotunda with <r>
        elif c in "Ʒ":
                text = text.replace(c, "Z") # replaces all instances of upper case <ezh> with <z>
        elif c in "ʒ":
                text = text.replace(c, "z") # replaces all instances of lower case <ezh> with <z>
        elif c in "ůüú":
                text = text.replace(c, "u") # normalises superscripts over <u>
        elif c in "óöò":
                text = text.replace(c, "o") # normalises superscripts over <o>
        elif c in "áä":
                text = text.replace(c, "a") # normalises supersripts over <a>
        elif c in "é":
                text = text.replace(c, "e") # normalises superscripts over <e>
        elif c in "⁄‧":
                text = text.replace(c,"") # removes original punctuation marks
        elif c in "#":
                text = text.replace(c, "[...]") # replaces all instances of <#> (unreadable characters) with <[...]>

with open (dest_dir/file_name, "w", encoding="utf8") as f:
        text=f.write(text) # saves the normalised xml file to destination directory

print(f"{file_name} saved to {dest_dir}.")