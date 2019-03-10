import re

proxy = """
🔘 DIRECT = direct



◻️ REJECT = reject
◼️ BLOCK = reject-tinygif

"""
line = "👾 Advertising = select, ◼️ BLOCK ,◻️ REJECT ,🔘 DIRECT"
split = re.search(
    r"(?P<name>.*) *= *(?P<type>[^,]*), *(?P<proxies>.*)", line)
reject = "◻️ REJECT"
tinygif = "◼️ BLOCK"
proxies_lines = split.group("proxies").split(',')
proxies = ""


for index in range(len(proxies_lines)):
    if (reject != "" and proxies_lines[index].find(reject) != -1) or (tinygif != "" and proxies_lines[index].find(tinygif) != -1):
        print("proxies_lines: $" +
              proxies_lines[index]+"$=>$"+"REJECT")
        proxies_lines[index] = "REJECT"
    proxies += "      - \""+proxies_lines[index].strip()+"\"\n"
print(proxies)
