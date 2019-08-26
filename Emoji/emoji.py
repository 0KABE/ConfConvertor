import abc
import base64
import json
import urllib
import urllib.parse
from enum import Enum

import emoji
import requests
from flask import Request, Response, make_response

DEFAULT_EMOJI_URL = "https://raw.githubusercontent.com/0KABE/ConfConvertor/master/Emoji/flag_emoji.json"
DEFAULT_FILE_NAME = "Emoji"


class EmojiParm(Enum):
    TYPE = "type"
    URL = "url"
    FILE_NAME = "filename"
    DEL_EMOJI = "delEmoji"
    DIRECTION = "direction"
    EMOJI = "emoji"


class EmojiType(Enum):
    SURGE_LIST = "surgelist"
    SS = "ss"
    SSR = "ssr"


class Direction(Enum):
    HEAD = "head"
    TAIL = "tail"


class Emoji(object):
    def __init__(self, request: Request):
        self.type: EmojiType = EmojiType(
            request.args.get(EmojiParm.TYPE.value, EmojiType.SURGE_LIST.value))
        self.url: str = request.args.get(EmojiParm.URL.value)
        self.filename: str = request.args.get(
            EmojiParm.FILE_NAME.value, DEFAULT_FILE_NAME)
        self.delete: bool = False if request.args.get(
            EmojiParm.DEL_EMOJI.value) == "false" else True
        self.direction: Direction = Direction(
            request.args.get(EmojiParm.DIRECTION.value, Direction.TAIL.value))
        self.emoji_url: str = request.args.get(
            EmojiParm.EMOJI.value, DEFAULT_EMOJI_URL)
        self.emoji_content: str = requests.get(self.emoji_url).content.decode()
        self.emoji: dict = json.loads(self.emoji_content)
        self.url_content: list = self._download_url_content()

    def convert(self) -> Response:
        if(self.delete):
            self._del_emoji()
        response: Response = make_response(
            "\n".join(self._add_emoji().url_content))
        response.headers["Content-Disposition"] = "attachment; filename="+self.filename
        return response

    def _download_url_content(self) -> list:
        return requests.get(self.url).content.decode().splitlines()

    def _add_emoji_by_line(self, line: str):
        index = None
        key = None
        for k in self.emoji.keys():
            for v in self.emoji[k]:
                if self.direction == Direction.TAIL:
                    pos = line.rfind(v)
                    if pos != -1 and (index == None or index < pos):
                        index = pos
                        key = k
                elif self.direction == Direction.HEAD:
                    pos = line.find(v)
                    if pos != -1 and (index == None or index > pos):
                        index = pos
                        key = k
        if index != None:
            return key+line
        else:
            return line

    @abc.abstractmethod
    def _add_emoji(self):
        pass

    @abc.abstractmethod
    def _del_emoji(self):
        pass


class SurgeListEmoji(Emoji):
    def _del_emoji(self):
        for i in range(len(self.url_content)):
            self.url_content[i] = emoji.get_emoji_regexp().sub(
                u'', self.url_content[i])
        return self

    def _add_emoji(self):
        res: list = []
        for line in self.url_content:
            res.append(self._add_emoji_by_line(line))
        self.url_content = res
        return self


class SSEmoji(Emoji):
    def _download_url_content(self):
        content: bytes = requests.get(self.url).content
        content_decoded: str = content.decode()
        if(content_decoded.startswith("ss://")):
            return content_decoded.splitlines()
        else:
            return base64.b64decode(content).decode().splitlines()

    def _node_name(self, url: str) -> str:
        return urllib.parse.unquote(urllib.parse.urlparse(url).fragment)

    def _del_emoji(self):
        for i in range(len(self.url_content)):
            url = self.url_content[i]
            parsed = urllib.parse.urlparse(url)
            parsed = parsed._replace(fragment=emoji.get_emoji_regexp().sub(
                u'', self._node_name(url)))
            self.url_content[i] = urllib.parse.urlunparse(parsed)
        return self

    def _add_emoji(self):
        res = []
        for url in self.url_content:
            parsed = urllib.parse.urlparse(url)
            name = self._add_emoji_by_line(self._node_name(url))
            parsed = parsed._replace(fragment=name)
            res.append(urllib.parse.urlunparse(parsed))
        self.url_content = res
        return self

    def convert(self) -> Response:
        if(self.delete):
            self._del_emoji()
        response: Response = make_response(
            base64.b64encode(
                "\n".join(self._add_emoji().url_content).encode()).decode())
        response.headers["Content-Disposition"] = "attachment; filename="+self.filename
        return response


class SSREmoji(SSEmoji):
    def _download_url_content(self):
        content: bytes = requests.get(self.url).content
        content_decoded = content.decode()
        if(content_decoded.startswith("ssr://")):
            return content_decoded.splitlines()
        else:
            # add missing padding
            content += b'='*(-len(content) % 4)
            return base64.urlsafe_b64decode(content).decode().splitlines()

    def _parse_ssr_url(self, url: str):
        # ssr://netloc -> netloc
        base64_content: str = urllib.parse.urlparse(url).netloc
        # add missing padding
        base64_content += '='*(-len(base64_content) % 4)
        # urlsafe base64 decode
        # decode bytes to str
        # add "ssr://" at the leading
        content: str = "ssr://" + \
            base64.urlsafe_b64decode(base64_content).decode()
        return content

    def _unparse_ssr_url(self, url: str):
        base64_content: str = url.replace("ssr://", "", 1)
        ssr_url = "ssr://" + \
            base64.urlsafe_b64encode(
                base64_content.encode()).decode().rstrip("=")
        return ssr_url

    def _node_name(self, url: str):
        # get parameter dictionary
        param_dict: dict = urllib.parse.parse_qs(
            urllib.parse.urlparse(url).query, keep_blank_values=True)
        # replace ' ' by '+'
        remarks = param_dict["remarks"][0].replace(' ', '+')
        # add missing padding
        # get the parameter remarks
        name: str = base64.urlsafe_b64decode(
            remarks+'='*(-len(remarks) % 4)).decode()
        return name

    def _del_emoji(self):
        res = []
        for url in self.url_content:
            url = self._parse_ssr_url(url)
            name = emoji.get_emoji_regexp().sub(
                u'', self._node_name(url))
            parsed = urllib.parse.urlparse(url)
            query: dict = urllib.parse.parse_qs(
                parsed.query)
            query["remarks"][0] = base64.urlsafe_b64encode(
                name.encode()).decode().rstrip("=")
            for key in query:
                query[key] = "".join(query[key])
            parsed = parsed._replace(query=urllib.parse.urlencode(query))
            res.append(self._unparse_ssr_url(urllib.parse.urlunparse(parsed)))
        self.url_content = res
        return self

    def _add_emoji(self):
        res = []
        for url in self.url_content:
            url = self._parse_ssr_url(url)
            name = self._add_emoji_by_line(self._node_name(url))
            parsed = urllib.parse.urlparse(url)
            query: dict = urllib.parse.parse_qs(
                parsed.query)
            query["remarks"][0] = base64.urlsafe_b64encode(
                name.encode()).decode().rstrip("=")
            for key in query:
                query[key] = "".join(query[key])

            parsed = parsed._replace(query=urllib.parse.urlencode(query))
            res.append(self._unparse_ssr_url(urllib.parse.urlunparse(parsed)))
            # res.append(urllib.parse.urlunparse(parsed))
        self.url_content = res
        return self

    def convert(self) -> Response:
        if(self.delete):
            self._del_emoji()
        response: Response = make_response(
            base64.urlsafe_b64encode(
                "\n".join(self._add_emoji().url_content).encode()).decode().rstrip("="))
        response.headers["Content-Disposition"] = "attachment; filename="+self.filename
        return response
