import xml.etree.ElementTree as ET


def GetRuleElement(line, policy_name=None):
    l = line.split(",")
    element = ET.Element(l[0].replace(" ", ""))
    if element.tag == "FINAL":
        if policy_name == None:
            element.set("policy", l[1])
        else:
            element.set("policy", policy_name)
        if "dns-failed" in l:
            element.set("dns-failed", "true")
    else:
        element.set("match", l[1].strip())
        if policy_name == None:
            element.set("policy", l[2])
        else:
            element.set("policy", policy_name)
        if "no-resolve" in l:
            element.set("no-resolve", "true")

    return element
