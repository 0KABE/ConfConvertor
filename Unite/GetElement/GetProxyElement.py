import xml.etree.ElementTree as ET


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
