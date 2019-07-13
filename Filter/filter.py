from flask import Request, make_response
import re
import abc
import requests


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
