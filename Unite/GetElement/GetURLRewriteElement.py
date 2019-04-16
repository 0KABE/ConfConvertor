import xml.etree.ElementTree as ET


def GetURLRewriteElement(line):
    l = line.split(" ", 3)
    element = ET.Element("Type_"+l[2])
    element.set("type", l[2])
    element.set("regex", l[0])
    element.set("replace", l[1])
    return element
