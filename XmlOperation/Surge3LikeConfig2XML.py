import xml.etree.ElementTree as ET
import xml.dom.minidom

CommentKeywords = ("#", ";", "//")
TypeKeywords = ("[General]", "[Replica]", "[Proxy]", "[Proxy Group]", "[Rule]",
                "[Host]", "[URL Rewrite]", "[Header Rewrite]", "[SSID Setting]", "[MITM]")


def GetGeneralElement(line):
    l = line.split("=")
    element = ET.Element(l[0].replace(" ", ""))
    element.text = l[1].strip()
    return element


def GetReplicaElement(line):
    l = line.split("=")
    element = ET.Element(l[0].replace(" ", ""))
    element.text = l[1].strip()
    return element


def GetProxyElement(line):
    Info_Correspond = {"ss": ("type", "server", "port", "encrypt-method", "password", "obfs", "obfs-host", "tfo", "udp-relay"),
                       "custom": ("type", "server", "port", "encrypt-method", "password", "module")}
    l = line.split("=", 1)
    if l[1].find(",") == -1:
        element = ET.Element("Built-in")
        element.set("name", l[0].strip())
        element.set("policy", l[1].strip())
    else:
        element = ET.Element("External")
        element.set("name", l[0].strip())
        info = l[1].split(",")
        ProxyType = info[0].strip()
        for i in range(len(info)):
            if info[i].find("=") == -1:
                element.set(Info_Correspond[ProxyType]
                            [i], info[i].strip())
            else:
                key = info[i].split("=")[0].strip()
                value = info[i].split("=")[1].strip()
                element.set(key, value)
    return element


def GetProxyGroupElement(line, remove=None):
    l = line.split("=", 1)
    values = l[1].split(",")
    element = ET.Element("policy")
    element.set("name", l[0].strip())
    for i in range(len(values)):
        if i == 0:
            if type(remove) == set and values[i].strip() == "load-balance":
                remove.add(element.get("name"))
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


def GetHostElement(line):
    l = line.split("=")
    element = ET.Element("Item")
    element.set("key", l[0].strip())
    element.set("value", l[1].strip())
    return element


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


def GetURLRewriteElement(line):
    l = line.split(" ", 3)
    element = ET.Element("Type_"+l[2])
    element.set("type", l[2])
    element.set("regex", l[0])
    element.set("replace", l[1])
    return element


def GetHeaderRewriteElement(line):
    l = line.split(" ", 3)
    element = ET.Element("Type_"+l[1])
    element.set("regex", l[0])
    element.set("field", l[2])
    if l[1] != "header-del":
        element.set("value", l[3])
    return element


def GetMITMElement(line):
    l = line.split("=", 1)
    element = ET.Element(l[0].replace(" ", ""))
    element.text = l[1].strip()
    return element


def Content2XML(content, remove=None):
    # f = open("OKAB3.conf", "r", encoding="utf-8")
    root = ET.Element("config")
    CurElement = root
    for line in content.splitlines():
        line = line.strip("\n")
        # 类型关键词
        if line in TypeKeywords:
            TypeIndex = {"General": "1", "Replica": "2", "Proxy": "3", "ProxyGroup": "4", "Rule": "5",
                         "Host": "6", "URLRewrite": "7", "HeaderRewrite": "8", "SSIDSetting": "9", "MITM": "10"}
            line = line.strip("[")
            line = line.strip("]")
            line = line.replace(" ", "")
            sub = ET.Element(line)
            sub.set("index", TypeIndex[line])
            root.append(sub)
            CurElement = root.find(line)
        # 备注
        elif line.startswith(CommentKeywords):
            temp = ET.Element("comment")
            temp.text = line
            if not line.startswith("#!MANAGED-CONFIG"):
                CurElement.append(temp)
        # 排除空行或者只有空白符
        elif line != "" and not line.isspace():
            if CurElement.tag == "General":
                CurElement.append(GetGeneralElement(line))
            elif CurElement.tag == "Replica":
                CurElement.append(GetReplicaElement(line))
            elif CurElement.tag == "Proxy":
                CurElement.append(GetProxyElement(line))
            elif CurElement.tag == "ProxyGroup":
                CurElement.append(GetProxyGroupElement(line, remove))
            elif CurElement.tag == "Rule":
                CurElement.append(GetRuleElement(line))
            elif CurElement.tag == "Host":
                CurElement.append(GetHostElement(line))
            elif CurElement.tag == "URLRewrite":
                CurElement.append(GetURLRewriteElement(line))
            elif CurElement.tag == "HeaderRewrite":
                CurElement.append(GetHeaderRewriteElement(line))
            elif CurElement.tag == "MITM":
                CurElement.append(GetMITMElement(line))
    # tree = ET.ElementTree(root)
    # # tree.write("test.xml", xml_declaration="true", encoding="utf-8")
    # result = xml.dom.minidom.parseString(
    #     ET.tostring(root)).toprettyxml()
    # open("Private_Demo.xml", "w", encoding="utf-8").write(result)
    # print(result)

    # return ET.tostring(root)
    return root

# if __name__ == "__main__":
#     tree = ET.ElementTree(root)
#     # tree.write("test.xml", xml_declaration="true", encoding="utf-8")
#     result = xml.dom.minidom.parseString(
#         ET.tostring(tree.getroot())).toprettyxml()
#     open("Private_Demo.xml", "w", encoding="utf-8").write(result)
