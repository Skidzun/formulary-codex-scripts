'''
This file contains various scripts used for cleaning
texts produced via ATR.
It is currently under devolpment, so various parts of
it will be altered in the near future
'''

#import os
import re

#current_dir = os.path.dirname(os.path.abspath(__file__))
#project_root = os.path.dirname(current_dir)
#data_dir = os.path.join(project_root, "data")

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

def remove_punctuation(txt):
    '''
    Function to remove punctuation.
    '''
    for c in "/‧":
        txt = txt.replace(c,"")
    
    return txt

