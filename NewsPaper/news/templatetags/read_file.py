import csv, enum, os

class Encoding(enum.Enum):
    UTF8 = "utf-8"
    ASCII = "ascii"
    CP1252 = "cp1252"
    ISO_88591 = "iso-8859-1"

def read_txt_as_list(localpath:str, encoding:Encoding):
    results = []
    formated_list = []
    with open(os.getcwd()+"\\" + localpath, newline='', encoding = str(encoding.value)) as inputfile:
        for row in csv.reader(inputfile):
            results.append(row)

    for list in results:
        for elem in list:
            if elem and elem.strip():
                formated_list.append(elem.strip())
    return formated_list