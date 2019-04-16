import xml.etree.ElementTree as ET


def GetMITMElement(line):
    l = line.split("=", 1)
    element = ET.Element(l[0].replace(" ", ""))
    element.text = l[1].strip()
    return element
