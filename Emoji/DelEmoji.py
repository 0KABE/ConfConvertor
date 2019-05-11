import emoji


def delete(line):
    return emoji.get_emoji_regexp().sub(u'', line)
