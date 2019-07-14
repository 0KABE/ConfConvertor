import abc
import base64
import re
import urllib.parse

import requests
from flask import Request, make_response


class Filter(object):
    def __init__(self, request: Request):
        self.filename: str = request.args.get("filename")
        self.regex: str = request.args.get("regex")
        self.rename: str = request.args.get("rename")
        self.url: str = request.args.get("url")
        self.type: str = request.args.get("type")

    @abc.abstractmethod
    def filter_source(self):
        return


class SrugeListFilter(Filter):
    def __init__(self, request: Request):
        super().__init__(request)
        if self.filename is None:
            self.filename = "Filter.list"

    def filter_proxy(self) -> str:
        """
        get all proxies from the url
        """
        # get the decoded content from the url
        # strip unnecessary whitespace
        return requests.get(
            self.url).content.decode().strip()

    def filter_by_regex(self, content: str) -> str:
        proxies: list = content.splitlines()
        prog = re.compile(self.regex)
        result: list = []  # filter result
        for line in proxies:
            math_group = prog.match(line)
            # if the line match the regex
            if math_group:
                # if need to rename
                if self.rename:
                    proxy: str
                    for part in self.rename.splitlines():
                        if part in math_group.groupdict():
                            proxy += math_group.group(part)
                        else:
                            proxy += part
                    result.append(proxy)
                else:
                    result.append(line)
        return "\n".join(result)

    def filter_source(self):
        response = make_response(self.filter_by_regex(self.filter_proxy()))
        response.headers["Content-Disposition"] = "attachment; filename="+self.filename
        return response


class SurgeConfFilter(SrugeListFilter):
    def filter_proxy(self) -> str:
        content: list = requests.get(
            self.url).content.decode().strip().splitlines()
        proxies: list = []
        status: str = ""
        for line in content:
            if line.startswith("["):
                status = line
            elif status == "[Proxy]":
                proxies.append(line)
        return "\n".join(proxies)


class SSFilter(Filter):
    def __init__(self, request):
        super().__init__(request)
        if self.filename is None:
            self.filename = "Filter.txt"

    def filter_source(self):
        response = make_response(self.filter_by_regex())
        response.headers["Content-Disposition"] = "attachment; filename="+self.filename
        return response

    def download_content(self):
        return base64.b64decode(
            requests.get(self.url).content).decode().splitlines()

    def filter_by_regex(self):
        content: list = self.download_content()
        prog = re.compile(self.regex)
        result: list = []  # filter result
        for line in content:
            name: str = self.node_name(line)
            match = prog.match(name)
            if match:
                result.append(line)
        return "\n".join(result).encode()

    def node_name(self, url: str) -> str:
        return urllib.parse.unquote(urllib.parse.urlparse(url).fragment)


class SSRFilter(SSFilter):
    def download_content(self):
        content: bytes = requests.get(self.url).content
        # add missing padding
        content += b'='*(-len(content) % 4)
        return base64.urlsafe_b64decode(content).decode().splitlines()

    def node_name(self, url: str):
        # ssr://netloc -> netloc
        base64_content: str = urllib.parse.urlparse(url).netloc
        # add missing padding
        base64_content += '='*(-len(base64_content) % 4)
        # urlsafe base64 decode
        # decode bytes to str
        # add "ssr://" at the leading
        content: str = "ssr://" + \
            base64.urlsafe_b64decode(base64_content).decode()
        # get parameter dictionary
        param_dict: dict = urllib.parse.parse_qs(
            urllib.parse.urlparse(content).query)
        # add missing padding
        # get the parameter remarks
        name: str = base64.urlsafe_b64decode(
            param_dict["remarks"][0]+'='*(-len(param_dict["remarks"][0]) % 4)).decode()
        return name
