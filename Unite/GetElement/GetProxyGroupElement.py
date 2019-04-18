import xml.etree.ElementTree as ET


def GetProxyGroupElement(line):
    l = line.split("=", 1)
    values = l[1].split(",")
    element = ET.Element("policy")
    element.set("name", l[0].strip())
    for i in range(len(values)):
        if i == 0:
            element.set("type", values[i].strip())
        elif values[i].find("=") != -1:
            option = values[i].split("=", 1)
            if option[0].strip() == "policy-path":
                sub = ET.Element("policy-path")
                sub.text = option[1].strip()
                element.append(sub)
            else:
                element.set(option[0].strip(), option[1].strip())
        else:
            sub = ET.Element("policy")
            sub.text = values[i].strip()
            element.append(sub)
    return element
