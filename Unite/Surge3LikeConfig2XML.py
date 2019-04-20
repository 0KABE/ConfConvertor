import xml.dom.minidom
import xml.etree.ElementTree as ET

from Unite.GetElement.GetGeneralElement import GetGeneralElement
from Unite.GetElement.GetHeaderRewriteElement import GetHeaderRewriteElement
from Unite.GetElement.GetHostElement import GetHostElement
from Unite.GetElement.GetMITMElement import GetMITMElement
from Unite.GetElement.GetProxyElement import GetProxyElement
from Unite.GetElement.GetProxyGroupElement import GetProxyGroupElement
from Unite.GetElement.GetReplicaElement import GetReplicaElement
from Unite.GetElement.GetRuleElement import GetRuleElement
from Unite.GetElement.GetURLRewriteElement import GetURLRewriteElement

CommentKeywords = ("#", ";", "//")
TypeKeywords = ("[General]", "[Replica]", "[Proxy]", "[Proxy Group]", "[Rule]",
                "[Host]", "[URL Rewrite]", "[Header Rewrite]", "[SSID Setting]", "[MITM]")


def Content2XML(content):
    # f = open("OKAB3.conf", "r", encoding="utf-8")
    root = ET.Element("config")
    CurElement = root
    for line in content.splitlines():
        TypeIndex = {"comment": "0", "General": "1", "Replica": "2", "Proxy": "3", "ProxyGroup": "4", "Rule": "5",
                     "Host": "6", "URLRewrite": "7", "HeaderRewrite": "8", "SSIDSetting": "9", "MITM": "10"}
        line = line.strip("\n")
        # 类型关键词
        if line in TypeKeywords:
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
            temp.set("index", TypeIndex["comment"])
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
                CurElement.append(GetProxyGroupElement(line))
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
    # result = xml.dom.minidom.parseString(
    #     ET.tostring(root)).toprettyxml()
    # open("Private_Demo.xml", "w", encoding="utf-8").write(result)
    return root

# if __name__ == "__main__":
#     tree = ET.ElementTree(root)
#     # tree.write("test.xml", xml_declaration="true", encoding="utf-8")
#     result = xml.dom.minidom.parseString(
#         ET.tostring(tree.getroot())).toprettyxml()
#     open("Private_Demo.xml", "w", encoding="utf-8").write(result)
