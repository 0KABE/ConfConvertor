import asyncio
import xml.etree.ElementTree as ET

import aiohttp

from XmlOperation.Surge3LikeConfig2XML import GetProxyElement


async def download(url, result):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()
            result[url] = text


def GetUrls(urls):
    result = {}
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    loop = asyncio.get_event_loop()
    tasks = [download(url, result) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    return result
