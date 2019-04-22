import re


def GetList(data, regex):
    prog = re.compile(regex)
    data_list = data.splitlines()
    result_list = []
    for line in data_list:
        if prog.match(line):
            result_list.append(line)
    return "\n".join(result_list)
