import re


def FromList(data, regex):
    prog = re.compile(regex)
    data_list = data.splitlines()
    result_list = []
    for line in data_list:
        if prog.match(line):
            result_list.append(line)
    return "\n".join(result_list)


def FromConfig(data, regex):
    prog = re.compile(regex)
    data_list = data.splitlines()
    result_list = []
    status = ""
    for line in data_list:
        if line.startswith('['):
            status = line
        elif status == "[Proxy]" and prog.match(line):
            result_list.append(line)
    return "\n".join(result_list)
