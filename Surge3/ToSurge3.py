import xml.etree.ElementTree as ET


def ToSurge3(root, remove=None):
    """
    Args:
        root(xml.etree.ElementTree.Element): the root element of the xml
    Return:
        A string contains Surge3Pro Configuration Content
    Do:
        Convert the content Surge3Pro-supported to String
    """
    Surge3 = ""
    KeyWordsCorrespond = {"General": "[General]", "Replica": "[Replica]", "Proxy": "[Proxy]", "ProxyGroup": "[Proxy Group]", "Rule": "[Rule]",
                          "Host": "[Host]", "URLRewrite": "[URL Rewrite]", "HeaderRewrite": "[Header Rewrite]", "SSIDSetting": "[SSID Setting]", "MITM": "[MITM]"}
    ProxyTypeAttrib = {"ss": {"type": "", "server": "", "port": "", "encrypt-method": "encrypt-method=", "password": "password=", "obfs": "obfs=", "obfs-host": "obfs-host=", "tfo": "tfo=", "udp-relay": "udp-relay="},
                       "custom": {"type": "", "server": "", "port": "", "encrypt-method": "", "password": "", "module": ""}}
    for elem in root:
        if elem.tag == "comment":
            continue
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
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                elif sub.tag == "Built-in":
                    Surge3 += sub.get("name")+" = "+sub.get("policy")+"\n"
                else:
                    ProxyType = sub.get("type")
                    if sub.get("type") in ProxyTypeAttrib:
                        l = list()
                        for key in ProxyTypeAttrib[ProxyType]:
                            if key in sub.attrib:
                                l.append(
                                    ProxyTypeAttrib[ProxyType][key]+sub.get(key))
                        Surge3 += sub.get("name")+" = "+", ".join(l)+"\n"
        elif elem.tag == "ProxyGroup":
            RequiredPara = ("name", "type")
            for sub in elem:
                if sub.tag == "comment":
                    Surge3 += sub.text+"\n"
                else:
                    if sub.get("name") in remove:
                        continue
                    l = list()
                    l.append(sub.get("type"))
                    for it in sub:
                        if it.text in remove:
                            continue
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
                    if sub.tag == "Type_header-del":
                        Surge3 += sub.get("regex")+" "+Type_Correspond[sub.tag]+" "+sub.get(
                            "field")+"\n"
                    else:
                        Surge3 += sub.get("regex")+" "+Type_Correspond[sub.tag]+" "+sub.get(
                            "field")+" "+sub.get("value")+"\n"
        elif elem.tag == "MITM":
            for sub in elem:
                Surge3 += sub.tag+" = "+sub.text+"\n"
    return Surge3
