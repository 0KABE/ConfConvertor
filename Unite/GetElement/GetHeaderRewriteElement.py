import xml.etree.ElementTree as ET


def GetHeaderRewriteElement(line):
    l = line.split(" ", 3)
    element = ET.Element("Type_"+l[1])
    element.set("regex", l[0])
    element.set("field", l[2])
    if l[1] != "header-del":
        element.set("value", l[3])
    return element
