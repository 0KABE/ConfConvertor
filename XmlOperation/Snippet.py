import requests
import yaml


def AddSnippet(url, dic):
    content = requests.get(url).text
    snippet = yaml.load(content)
    dic = {**dic, **snippet}
    return dic
