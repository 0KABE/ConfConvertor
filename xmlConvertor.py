import xml.etree.ElementTree as ET

general_KeyWords = {"Surge3": ["allow-wifi-access", "dns-server", "ipv6", "loglevel", "skip-proxy", "use-default-policy-if-wifi-not-primary",
                               "proxy-settings-interface", "always-real-ip", "hijack-dns", "tun-excluded-routes", "tun-included-routes"]}
replica_KeyWords = {"Surge3": [
    "hide-apple-request", "hide-crashlytics-request", "hide-udp", "use-keyword-filter"]}
rule_KeyWords = {"Surge3": ["DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "GEOIP", "USER-AGENT",
                            "URL-REGEX", "PROCESS-NAME", "AND", "OR", "NOT", "DEST-PORT", "SRC-IP", "IN-PORT", "RULE-SET", "FINAL"]}


def Surge3Pro(tree):
    #get [General]
    general_elem = tree.find("General")
    general_str = "[General]\n"
    for elem in general_elem.iter():
        if elem.tag in general_KeyWords["Surge3"]:
            general_str += elem.tag+" = "+elem.text+"\n"

    #get [Replica]
    replica_elem = tree.find("Replica")
    replica_str = "\n[Replica]\n"
    for elem in replica_elem.iter():
        if elem.tag in replica_KeyWords["Surge3"]:
            replica_str += elem.tag+" = "+elem.text+"\n"

    #get [Proxy]
    proxy_elem = tree.find("Proxy")
    proxy_str = "\n[Proxy]\n"
    for elem in proxy_elem:
        proxy_str += elem.text+" = "+elem.tag+"\n"

    # get [Proxy Group]
    proxy_group_elem = tree.find("Proxy_Group")
    proxy_group_str = "\n[Proxy Group]\n"
    for elem in proxy_group_elem.iter("Group"):
        proxy_group_str += elem.get("name")+" = "+elem.get("type")
        for i in elem.iter("policy-path"):
            proxy_group_str += ", "+i.tag+" = "+i.get("url")
        for i in elem.iter("proxies"):
            proxy_group_str += ", "+i.text
        if elem.get("type") != "select":
            if(elem.get("url")):
                proxy_group_str += ", url = "+elem.get("url")
            if elem.get("interval"):
                proxy_group_str += ", interval = "+elem.get("interval")
            if elem.get("tolerance"):
                proxy_group_str += ", tolerance = "+elem.get("tolerance")
            if elem.get("timeout"):
                proxy_group_str += ", timeout = "+elem.get("timeout")
        proxy_group_str += "\n"
    #get [Rule]
    rule_elem = tree.find("Rule")
    rule_str = "\n[Rule]\n"
    for elem in rule_elem:
        if elem.tag in rule_KeyWords["Surge3"]:
            rule_str += elem.tag+", "+elem.text + \
                ", "+elem.get("proxy_group")+"\n"

    ##
    print(general_str+replica_str+proxy_str+proxy_group_str+rule_str)
    return general_str+replica_str+proxy_str+proxy_group_str+rule_str


f = open("Demo.xml", "r", encoding="utf-8")
tree = ET.fromstring(f.read())

conf = Surge3Pro(tree)
