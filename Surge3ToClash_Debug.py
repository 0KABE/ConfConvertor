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
    proxy += "\n".join(list(sorted(proxy_dic.values())))
    proxy += "\n\n"

    direct = ""
    reject = ""
    tinygif = ""
    temp = re.search("(.*?) *= *direct", proxy)
    if temp:
        direct = temp.group(1)
    temp = re.search("(.*?) *= *reject", proxy)
    if temp:
        reject = temp.group(1)
    temp = re.search("(.*?) *= *reject-tinygif", proxy)
    if temp:
        tinygif = temp.group(1)

    return proxy_group, proxy, direct, reject, tinygif


def proxy_to_clash(proxy):
    converted = "Proxy:\n"
    pattern = re.compile(
        "(?P<name>.*?) *= *(?P<type>[^,]*), *(?P<server>[^,]*), *(?P<port>[^,]*), *encrypt-method *= *(?P<cipher>[^,]*), *password *= *(?P<password>[^,]*), *obfs *= *(?P<obfs>[^,]*)")
    lines = proxy.splitlines()
    for line in lines:
        result = pattern.search(line)
        if result == None:
            continue
        converted += "  - type: "+result.group("type")+"\n    name: \""+result.group("name") + "\"\n    server: "+result.group("server")+"\n    port: \'"+result.group(
            "port") + "\'\n    cipher: "+result.group("cipher")+"\n    password: "+result.group("password")+"\n    obfs: "+result.group("obfs")+"\n"

    return converted


def proxy_group_to_clash(proxy_group, reject, tinygif):
    converted = "Proxy Group:\n"
    proxy_group_list = proxy_group.splitlines()
    for line in proxy_group_list:
        if len(line) == 0 or line[0] in ['#', '[', '/']:
            continue
        test_exist_url = re.search(r"url *=", line)
        if test_exist_url != None:
            split = re.search(
                r"(?P<name>.*?) *= *(?P<type>[^,]*), *(?P<proxies>.*), *(?=url *=)(?P<parameter>.*)", line)
            temp = re.search(r"url *= *([^,]*)", line)
            url = "http://www.gstatic.com/generate_204"
            interval = "600"
            if temp:
                url = temp.group(1)
            temp = re.search(r"interval *= *([^,]*)", line)
            if temp:
                interval = temp.group(1)

            proxies_lines = split.group("proxies").split(',')
            proxies = ""
            for index in range(len(proxies_lines)):
                proxies += "      - \""+proxies_lines[index].strip()+"\"\n"
            converted += "  - name: \"" + \
                split.group("name").strip()+"\"\n    type: " + \
                split.group("type")+"\n    proxies:\n"+proxies
            if url:
                converted += "    url: \'"+url+"\'\n"
            if interval:
                converted += "    interval: \'"+interval+"\'\n"

            # print("\n\nname: "+split.group(1))
            # print("\n\ntype: "+split.group(2))
            # print("\n\nproxies: "+split.group(3))
            # print("\n\nparameter: "+split.group(4))

        else:
            split = re.search(
                r"(?P<name>.*) *= *(?P<type>[^,]*), *(?P<proxies>.*)", line)
            proxies_lines = split.group("proxies").split(',')
            proxies = ""
            for index in range(len(proxies_lines)):
                proxies += "      - \""+proxies_lines[index].strip()+"\"\n"
            converted += "  - name: \"" + \
                split.group("name").strip()+"\"\n    type: " + \
                split.group("type")+"\n    proxies:\n"+proxies
        #     print("\n\nname: "+split.group(1))
        #     print("\n\ntype: "+split.group(2))
        #     print("\n\nproxies: "+split.group(3))
        # print("\n\nconverted:\n"+converted)
    return converted


def rule_to_clash(rule):
    support_prefix = ["DOMAIN-SUFFIX", "DOMAIN",
                      "IP-CIDR", "DOMAIN-KEYWORD", "GEOIP", "FINAL"]
    converted = "Rule:\n"
    rule_lines = rule.splitlines()
    for line in rule_lines:
        for i in support_prefix:
            if line.startswith(i):
                if i == "FINAL":
                    converted += "  - \"MATCH,"+line.split(',')[1]+"\"\n"
                else:
                    converted += "  - \""+line+"\"\n"
    return converted


def Surge3ToClash(content):
    # 处于[Proxy]前面的配置
    front = "port: 7890\nsocks-port: 7891\nredir-port: 0\nallow-lan: false\nmode: Rule\nlog-level: info\nexternal-controller: '0.0.0.0:9090'\nsecret: ''\n"
    # [Proxy]的配置
    proxy = re.search(
        r"\[Proxy\](.|\r|\n)[^\[]*", content).group()
    # [Proxy Group]的配置
    proxy_group = re.search(
        r"\[Proxy Group\][^\[]*", content).group()
    proxy_group, proxy, direct, reject, tinygif = Proxy_Group(
        proxy_group, proxy)
    proxy = proxy_to_clash(proxy)
    proxy_group = proxy_group_to_clash(proxy_group, reject, tinygif)

    # [Rule]的配置
    rule = re.search(r"\[Rule\][^\[]*", content).group()
    rule = RuleSet(rule)
    rule = rule_to_clash(rule)
    # 替换direct tinygif reject
    if direct != "":
        rule = rule.replace(direct, "DIRECT")
        proxy_group = proxy_group.replace("\""+direct+"\"", "DIRECT")
    rule = rule.replace(",no-resolve", "")
    rule = rule.replace(",force-remote-dns", "")
    if reject != "":
        rule = rule.replace("\""+reject+"\"", "REJECT")
        proxy_group = proxy_group.replace("\""+reject+"\"", "REJECT")
    if tinygif != "":
        rule = rule.replace("\""+tinygif+"\"", "REJECT")
        proxy_group = proxy_group.replace("\""+tinygif+"\"", "REJECT")

    return front+proxy+proxy_group+rule


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
    response.headers["Content-Disposition"] = "attachment; filename=config.yml"
    return response


# Code for debug locally, do not sync to the cloud function platform
if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=5000)
