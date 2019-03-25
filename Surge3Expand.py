from flask import Flask
from flask import request
from flask import Response
from flask import make_response
import requests
import re

app = Flask(__name__)


def RuleSet(rule):
    # 例外的URL
    exception_url = ["SYSTEM", "LAN"]
    pattern = re.compile("RULE-SET *, *([^,\n]*) *, *([^,\n]*)")
    rule = rule.splitlines()
    for index in range(len(rule)):
        result = re.search(pattern, rule[index])
        if result != None:
            url = result.group(1)
            proxy_group = result.group(2)
            if url in exception_url:
                continue
            download = bytes.decode(requests.get(url).content)
            download_list = download.splitlines()
            for i in range(len(download_list)):
                if len(download_list[i]) > 0 and download_list[i][0] not in ['#']:
                    download_list[i] += ","+proxy_group
            rule[index] = "\n".join(download_list)

    # 将list转化为string
    rule = "\n".join(rule)
    rule += "\n"
    return rule


def Proxy_Group(proxy_group, proxy):
    pattern = re.compile("(.*)policy-path *= *([^ ,\n]*)(.*)")
    proxy_group = proxy_group.splitlines()
    proxy_dic = dict()

    for index in range(len(proxy_group)):
        result = re.search(pattern, proxy_group[index])
        if result != None:
            grouphead = result.group(1)
            url = result.group(2)
            groupback = result.group(3)
            download = bytes.decode(requests.get(url).content)
            download_list = download.splitlines()
            for i in range(len(download_list)):
                name = download_list[i].split('=', 1)[0]
                proxy_dic[name] = download_list[i]
                download_list[i] = name
            proxy_group[index] = grouphead+",".join(download_list)+groupback
    # 将list转化为string
    proxy_group = "\n".join(proxy_group)
    proxy_group += "\n\n"
    proxy += list(sorted(proxy_dic.values()))
    return proxy_group, proxy


def Surge3ToClash(content):
    # 处于[Proxy]前面的配置
    front = re.search(r"^(.|\r|\n)*(?=\[Proxy\])", content).group()
    # [Proxy]的配置
    proxy = re.search(
        r"\[Proxy\]([^\[]*)", content).group(1)
    proxy = proxy.strip("\n")
    proxy = proxy.splitlines()
    proxy = list(set(proxy))
    # [Proxy Group]的配置
    proxy_group = re.search(
        r"\[Proxy Group\][^\[]*", content).group()
    proxy_group, proxy = Proxy_Group(proxy_group, proxy)
    # [Rule]的配置
    rule = re.search(r"\[Rule\][^\[]*", content).group()
    rule = RuleSet(rule)
    # 处于[Rule]后面的配置
    back = re.search(r"\[Host\](.|\r|\n)*", content)
    if back != None:
        back = back.group()
    else:
        back = ""
    # Proxy去重
    proxy = sorted(proxy)
    proxy = "[Proxy]\n" + "\n".join(proxy)+"\n\n"
    return front+proxy+proxy_group+rule+back


@app.route('/', methods=['GET', 'POST'])
# Cloud Function: def main(request):
# Local debug: def main():
def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        #flask.Flask.make_response>`.
        `make_response <http://flask.pocoo.org/docs/1.0/api/
    """
    url = request.args.get('url')
    content = requests.get(url).content
    content = bytes.decode(content)
    response = make_response(Surge3ToClash(content))
    response.headers["Content-Disposition"] = "attachment; filename=config.conf"
    return response


# Code for debug locally, do not sync to the cloud function platform
if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=5000)
