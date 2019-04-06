import xml.etree.ElementTree as ET
import xml.dom.minidom
import copy

from XmlOperation.GetUrlContent import GetUrls
from XmlOperation.Surge3LikeConfig2XML import GetRuleElement

CommentKeywords = ("#", ";", "//")
InternalRule = {
    "SYSTEM": """USER-AGENT,*com.apple.mobileme.fmip1
USER-AGENT,*WeatherFoundation*
USER-AGENT,%E5%9C%B0%E5%9B%BE*
USER-AGENT,%E8%AE%BE%E7%BD%AE*
USER-AGENT,com.apple.geod*
USER-AGENT,com.apple.Maps
USER-AGENT,FindMyFriends*
USER-AGENT,FindMyiPhone*
USER-AGENT,FMDClient*
USER-AGENT,FMFD*
USER-AGENT,fmflocatord*
USER-AGENT,geod*
USER-AGENT,locationd*
USER-AGENT,Maps*
DOMAIN,api.smoot.apple.com
DOMAIN,captive.apple.com
DOMAIN,configuration.apple.com
DOMAIN,guzzoni.apple.com
DOMAIN,smp-device-content.apple.com
DOMAIN,xp.apple.com
DOMAIN-SUFFIX,ess.apple.com
DOMAIN-SUFFIX,push-apple.com.akadns.net
DOMAIN-SUFFIX,push.apple.com
DOMAIN,aod.itunes.apple.com
DOMAIN,mesu.apple.com
DOMAIN,api.smoot.apple.cn
DOMAIN,gs-loc.apple.com
DOMAIN,mvod.itunes.apple.com
DOMAIN,streamingaudio.itunes.apple.com
DOMAIN-SUFFIX,lcdn-locator.apple.com
DOMAIN-SUFFIX,lcdn-registration.apple.com
DOMAIN-SUFFIX,ls.apple.com
PROCESS-NAME,trustd""",
    "LAN": """DOMAIN-SUFFIX,local
IP-CIDR,192.168.0.0/16
IP-CIDR,10.0.0.0/8
IP-CIDR,172.16.0.0/12
IP-CIDR,127.0.0.0/8
IP-CIDR,100.64.0.0/10"""}


def GetKey(elem):
    return int(elem.get("index"))


def ExpandRuleSet(root):
    urls = set()
    url_dict = {}
    for elem in root.findall("Rule/RULE-SET"):
        url = elem.get("match")
        if url not in InternalRule:
            urls.add(elem.get("match"))
    if urls:
        url_dict = GetUrls(urls)
    url_dict["SYSTEM"] = InternalRule["SYSTEM"]
    url_dict["LAN"] = InternalRule["LAN"]
    # parent = root.find("Rule")
    Rule = root.find("Rule")
    # parent = ET.Element("Rule")
    parent = ET.Element("Rule")
    parent.set("index", Rule.get("index"))
    for i in range(len(Rule.getchildren())):
        elem = Rule[i]
        if elem.tag != "RULE-SET":
            parent.append(elem)
            continue
        for line in url_dict[elem.get("match")].splitlines():
            if line.isspace() or line == "" or line.startswith(CommentKeywords):
                continue
            e = GetRuleElement(line, elem.get("policy"))
            parent.append(e)
    root.remove(Rule)
    root.append(parent)
    root[:] = sorted(root.getchildren(), key=GetKey)

    # result = xml.dom.minidom.parseString(
    #     ET.tostring(root)).toprettyxml()
    # open("Private_Demo.xml", "w", encoding="utf-8").write(result)
    return root
