import xml.etree.ElementTree as ET


def GetHostElement(line):
    l = line.split("=")
    element = ET.Element("Item")
    element.set("key", l[0].strip())
    element.set("value", l[1].strip())
    return element
