import xml.dom.minidom
import xml.etree.ElementTree as ET

visit = set()


def dfs(root, elem):
    visit.add(elem.get("name"))
    result = list()
    for it in elem:
        name = it.text
        if name in visit:
            continue
        for i in root.findall("ProxyGroup/policy"):
            if i.get("name") == name:
                result += dfs(root, i)
                break
    result.append(elem)
    return result


def TopologicalSort(root):
    ProxyGroup = root.find("ProxyGroup")
    result = list()
    for it in ProxyGroup:
        if it.get("name") not in visit:
            result += dfs(root, it)
    ProxyGroup[:] = result
    result = xml.dom.minidom.parseString(
        ET.tostring(root)).toprettyxml()
    return root
