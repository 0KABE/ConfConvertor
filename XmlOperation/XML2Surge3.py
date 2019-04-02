import xml.etree.ElementTree as ET
import requests
from XmlOperation.Surge3LikeConfig2XML import GetProxyElement
from XmlOperation.GetUrlContent import GetUrls


def NotExpand(root):
    Surge3 = ""
    KeyWordsCorrespond = {"General": "[General]", "Replica": "[Replica]", "Proxy": "[Proxy]", "ProxyGroup": "[Proxy Group]", "Rule": "[Rule]",
                          "Host": "[Host]", "URLRewrite": "[URL Rewrite]", "HeaderRewrite": "[Header Rewrite]", "SSIDSetting": "[SSID Setting]", "MITM": "[MITM]"}
    for elem in root:
        Surge3 += KeyWordsCorrespond[elem.tag]+"\n"
        if elem.tag == "General":
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                else:
                    Surge3 += sub.tag+" = "+sub.text+"\n"
        elif elem.tag == "Replica":
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                else:
                    Surge3 += sub.tag+" = "+sub.text+"\n"
        elif elem.tag == "Proxy":
            RequiredPara = ("type", "server", "port")
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                elif sub.tag == "Built-in":
                    Surge3 += sub.get("name")+" = "+sub.get("policy")+"\n"
                else:
                    if sub.get("type") == "ss":
                        l = list()
                        for it in RequiredPara:
                            l.append(sub.get(it))
                        for it in sub.attrib:
                            if it in RequiredPara or it == "name":
                                continue
                            l.append(it+" = "+sub.get(it))
                        Surge3 += sub.get("name")+" = "+", ".join(l)+"\n"
        elif elem.tag == "ProxyGroup":
            RequiredPara = ("name", "type")
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                else:
                    l = list()
                    l.append(sub.get("type"))
                    for it in sub:
                        if it .tag == "policy-path":
                            l.append("policy-path = "+it.text)
                        else:
                            l.append(it.text)
                    for it in sub.attrib:
                        if it in RequiredPara:
                            continue
                        l.append(it+" = "+sub.get(it))
                    Surge3 += sub.get("name")+" = "+", ".join(l)+"\n"
        elif elem.tag == "Rule":
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                elif sub.tag == "FINAL":
                    Surge3 += sub.tag+", "+sub.get("policy")
                    if "dns-failed" in sub.attrib and sub.attrib["dns-failed"] == "true":
                        Surge3 += ", dns-failed"
                    Surge3 += "\n"
                else:
                    Surge3 += sub.tag+", " + \
                        sub.get("match")+", "+sub.get("policy")+"\n"
        elif elem.tag == "Host":
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                else:
                    Surge3 += sub.get("key")+" = "+sub.get("value")+"\n"
        elif elem.tag == "URLRewrite":
            Type_Correspond = {"Type_302": "302", "Type_reject": "reject",
                               "Type_header": "header", "Type_307": "307"}
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                else:
                    Surge3 += sub.get("regex")+" "+sub.get("replace") + \
                        " "+Type_Correspond[sub.tag]+"\n"
        elif elem.tag == "HeaderRewrite":
            Type_Correspond = {"Type_header-replace": "header-replace",
                               "Type_header-add": "header-add", "Type_header-del": "header-del"}
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                else:
                    Surge3 += sub.get("regex")+" "+Type_Correspond[sub.tag]+" "+sub.get(
                        "field")+" "+sub.get("value")+"\n"
        elif elem.tag == "MITM":
            for sub in elem:
                Surge3 += sub.tag+" = "+sub.text+"\n"
    return Surge3


def Expand(root):
    urls = list()
    # result = {}
    for parent in root.findall("ProxyGroup/policy"):
        for it in parent.iter("policy-path"):
            urls.append(it.text)
            # result[it.text] = ""
    result = GetUrls(urls)
    # for it in result.keys():
    #     print("Downloading: "+it)
    #     result[it] = requests.get(it).content.decode()
    for parent in root.findall("ProxyGroup/policy"):
        for it in parent.findall("policy-path"):
            content = result[it.text]
            # content=requests.get(it.text).text
            for line in content.splitlines():
                elem = GetProxyElement(line)
                # Append the policy instead of the policy-path
                temp = ET.Element("policy")
                temp.text = elem.get("name")
                parent.append(temp)
                # check if exist the node
                exist = False
                for node in root.findall("Proxy/External"):
                    if node.get("name") == elem.get("name") and node.get("type") == elem.get("type"):
                        exist = True
                for node in root.findall("Proxy/Built-in"):
                    if node.get("name") == elem.get("name") and node.get("policy") == elem.get("policy"):
                        exist = True
                ######
                if not exist:
                    root.find("Proxy").append(elem)
            parent.remove(it)

    Surge3 = NotExpand(root)
    return Surge3


def XML2Surge3(x):
    # tree = ET.parse("Private_Demo.xml")
    # root = tree.getroot()
    root = ET.fromstring(x)

    expand = False
    # check if need to expand the policy-path
    Proxies = root.findall("ProxyGroup/policy")
    for elem in Proxies:
        sub = elem.findall("policy-path")
        if len(sub) > 1:
            expand = True
            break

    if not expand:
        Surge3 = NotExpand(root)
    else:
        Surge3 = Expand(root)

    # print(Surge3)
    return Surge3
