import xml.etree.ElementTree as ET


def GetReplicaElement(line):
    l = line.split("=")
    element = ET.Element(l[0].replace(" ", ""))
    element.text = l[1].strip()
    return element
