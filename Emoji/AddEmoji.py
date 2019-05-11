def fromTail(data, emoji_dict):
    data_list = data.splitlines()
    res = []
    for line in data_list:
        emoji = dict()
        emoji["index"] = None
        emoji["key"] = None
        for key in emoji_dict.keys():
            for value in emoji_dict[key]:
                pos = line.rfind(value)
                if pos != -1 and (emoji["index"] == None or emoji["index"] < pos):
                    emoji["index"] = pos
                    emoji["key"] = key
        if emoji["index"]:
            res.append(emoji["key"]+line)
        else:
            res.append(line)

    return "\n".join(res)


def fromHead(data, emoji_dict):
    data_list = data.splitlines()
    res = []
    for line in data_list:
        emoji = dict()
        emoji["index"] = None
        emoji["key"] = None
        for key in emoji_dict.keys():
            for value in emoji_dict[key]:
                pos = line.find(value)
                if pos != -1 and (emoji["index"] == None or emoji["index"] > pos):
                    emoji["index"] = pos
                    emoji["key"] = key
        if emoji["index"]:
            res.append(emoji["key"]+line)
        else:
            res.append(line)

    return "\n".join(res)
