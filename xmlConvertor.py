import xml.etree.ElementTree as ET


def Surge3(root):
    General = "[General]\n"
    for child in root.find("General"):
        Default_Keywords = {"ipv6": "false", "loglevel":
                            "notify", "allow-wifi-access": "false", "show-error-page-for-reject": "false"}
        tag = child.tag
        if tag in Default_Keywords:
            General += tag+" = "+child.get("value", Default_Keywords[tag])+"\n"
        elif tag == "skip-proxy":
            General += tag+" = "
            temp = list()
            for child in child.findall("Item"):
                temp.append(child.text)
            General += ", ".join(temp)+"\n"
        elif tag == "dns-server":
            General += tag+" = "
            temp = list()
            for child in child.findall("Item"):
                temp.append(child.text)
            General += ", ".join(temp)+"\n"

    Replica = "[Replica]\n"
    for child in root.find("Replica"):
        Default_Keywords = {"hide-apple-request": "true",
                            "hide-crashlytics-request": "true", "hide-udp": "false"}
        tag = child.tag
        if tag in Default_Keywords:
            Replica += tag+" = "+child.text+"\n"

    Proxies = "[Proxy]\n"
    for child in root.find("Proxies"):
        tag = child.tag
        if tag == "Built-in":
            Proxies += child.get("key")+" = "+child.get("value")+"\n"

    ProxyGroup = "[Proxy Group]\n"
    for child in root.find("PolicyGroup"):
        PolicyType = child.get("type")
        ProxyGroup += child.get("name")+" = "
        temp = list()
        temp.append(PolicyType)
        for child in child.iter("policy-path"):
            temp.append(child.tag+" = "+child.text)
        for child in child.iter("policy"):
            temp.append(child.text)
        if PolicyType == "fallback":
            temp.append("url = " +
                        child.get("url", "http://www.gstatic.com/generate_204"))
            temp.append(child.get("timeout", "5"))
        elif PolicyType == "url-test":
            temp.append("url = " +
                        child.get("url", "http://www.gstatic.com/generate_204"))
            temp.append("timeout = "+child.get("timeout", "5"))
            temp.append("tolerance = "+child.get("tolerance", "100"))
            temp.append("interval = "+child.get("interval", "600"))
        ProxyGroup += ", ".join(temp)+"\n"

    Rule = "[Rule]\n"
    for child in root.find("Rules"):
        KeyWords = ["USER-AGENT", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "GEOIP", "IP-CIDR", "USER-AGENT",
                    "URL-REGEX", "PROCESS-NAME", "AND", "OR", "NOT", "DEST-PORT", "SRC-IP", "IN-PORT", "RULE-SET", "FINAL"]
        if child.tag in KeyWords:
            if child.tag == "FINAL":
                Rule += child.tag+", "+child.get("policy")
                if "dns-failed" in child.attrib and child.get("dns-failed") == "true":
                    Rule += ", dns-failed"
            else:
                Rule += child.tag+", " + \
                    child.get("value")+", "+child.get("policy")

            if "notification-text" in child.attrib:
                Rule += ", notification-text = \"" + \
                    child.get("notification-text")+"\""
            if "notification-interval" in child.attrib:
                Rule += ", notification-interval = " + \
                    child.get("notification-interval")
            Rule += "\n"

    Host = "[Host]\n"
    for child in root.find("Host"):
        if child.tag == "Server":
            Host += child.get("key")+" = server:"+child.get("value")+"\n"

    UrlRewrite = "[URL Rewrite]\n"
    for child in root.find("UrlRewrite"):
        UrlRewrite += child.get("expression")+" " + \
            child.get("replacement")+" "+child.get("type")+"\n"

    HeaderRewrite = "[Header Rewrite]\n"
    for child in root.find("HeaderRewrite"):
        HeaderRewrite += child.get("field")+" " + \
            child.get("type") + " " + child.get("value")+"\n"

    Mitm = "[MITM]\n"
    Mitm += "enable = " + root.find("MITM").get("enable")+"\n"
    Mitm += "skip-server-cert-verify = " + \
        root.find("MITM").get("skip-server-cert-verify")+"\n"
    Mitm += "ca-passphrase = " + root.find("MITM/ca-passphrase").text+"\n"
    Mitm += "hostname = "
    l = list()
    for item in root.find("MITM/hostname"):
        l.append(item.text)
    Mitm += ", ".join(l)+"\n"

    return General+Replica+Proxies+ProxyGroup+Rule+UrlRewrite+HeaderRewrite+Mitm


f = open("Private_Demo.xml", "r", encoding="utf-8")
data = f.read()
root = ET.fromstring(data)
f = open("test.conf", "w", encoding="utf-8")
f.write(Surge3(root))

# print(Surge3(root))
