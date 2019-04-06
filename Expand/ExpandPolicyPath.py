import xml.etree.ElementTree as ET

from XmlOperation.GetUrlContent import GetUrls
from XmlOperation.Surge3LikeConfig2XML import GetProxyElement


def ExpandPolicyPath(root):
    """
    Args:
        root(xml.etree.ElementTree): the root element of the xml
    Return:
        the root element has been converted
    Do:
        Traverse all policy-path
        Add them to Element: Proxy
        Del the policy-path element
    """
    urls = list()
    # result = {}
    for parent in root.findall("ProxyGroup/policy"):
        for it in parent.iter("policy-path"):
            urls.append(it.text)
            # result[it.text] = ""
    if urls:
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

    return root
