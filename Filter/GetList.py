import re


def Regex(data_list, regex, rename):
    prog = re.compile(regex)
    result_list = []
    for line in data_list:
        group = prog.match(line)
        if group and rename:
            append = ""
            for sub in rename:
                if sub in group.groupdict():
                    append += group.group(sub)
                else:
                    append += sub
            result_list.append(append)
        elif group:
            result_list.append(line)
    return "\n".join(result_list)


def FromList(data, regex, rename):
    proxy_list = data.splitlines()
    return Regex(proxy_list, regex, rename)


def FromConfig(data, regex, rename):
    data_list = data.splitlines()
    proxy_list = []
    status = ""
    for line in data_list:
        if line.startswith('['):
            status = line
        elif status == "[Proxy]":
            proxy_list.append(line)
    return Regex(proxy_list, regex, rename)
