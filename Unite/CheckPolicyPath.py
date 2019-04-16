import xml.etree.ElementTree as ET
import requests


def NeedExpandPolicyPath(root):
    expand = False
    # check if need to expand the policy-path
    Proxies = root.findall("ProxyGroup/policy")
    for elem in Proxies:
        sub = elem.findall("policy-path")
        if len(sub) >= 1 and len(elem.getchildren()) > 1:
            expand = True
            break
    return expand
