import csv
import datetime
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment

import pandas as pd


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


generated_on = str(datetime.datetime.now())
# Configure one attribute with set()
root = Element('adlibXML')

root.append(Comment("Generated by xlsxToAdlibXML.py for NLI-VC"))
adlibXml = SubElement(root, 'adlibXml')
recordList = SubElement(adlibXml, 'recordList')

# open the xlsx as pandas Dataframe
Data_file = "Data/thesaurus1.xlsx"
xl = pd.ExcelFile(Data_file)
df = xl.parse("Thesaurus")
df.to_csv("thesaurus.csv", sep=',', encoding='utf-8', index=False)

with open('thesaurus.csv', 'rt', encoding='utf-8') as f:
    current_record = None
    reader = csv.reader(f)
    firstline = True
    for row in reader:
        if firstline:
            firstline = False
            continue

        prefLabelHeb, prefLabelEng, identifier, broader, altLabelHeb, altLabelEng, scopeNote, Collection, changeNote = row
        for item in row:
            print(item)
        current_record = SubElement(recordList, 'record')
        SubElement(current_record, "term.type").text = Collection
        SubElement(current_record, "term.code").text = identifier
        SubElement(current_record, "term.status").text = '1'
        SubElement(current_record, "term", {'lang': 'he-IL', 'occurrence': '1'}).text = prefLabelHeb
        SubElement(current_record, "term", {'lang': 'en-US', 'occurrence': '1'}).text = prefLabelEng
        SubElement(current_record, "scope_note").text = scopeNote
        SubElement(current_record, "change_note").text = changeNote
        if broader is not None:
            broader_terms = broader.split(';')
            for broader_term in broader_terms:
                SubElement(current_record, "relations.broader_term").text = broader_term
        if altLabelHeb is not None:
            alt_labels_heb = altLabelHeb.split(';')
            for alt_label_heb in alt_labels_heb:
                SubElement(current_record, "relations.used_for", {'lang': 'he-IL'}).text = alt_label_heb
        if altLabelEng is not None:
            alt_labels_eng = altLabelEng.split(';')
            for alt_label_eng in alt_labels_eng:
                SubElement(current_record, "relations.used_for", {'lang': 'en-US'}).text = alt_label_eng
        SubElement(current_record, "relations.broader_term", {'lang': 'heb-IL'}).text = scopeNote

with open('NLI-VC-Thesaurus_adlibXML.xml', 'w', encoding='utf-8') as file:
    file.write(prettify(root))
