import asyncio
import aiohttp
from mylocalpackage.Surge3LikeConfig2XML import GetProxyElement
import xml.etree.ElementTree as ET

result = {}


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print("Downloading:"+url)
            text = await resp.text()
            print("Downloade Completed:"+url)
            result[url] = text
            # result[url] = await resp.text()

           # print('\n\n', await resp.text())


def GetUrls(urls):
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    loop = asyncio.get_event_loop()
    tasks = [download(url) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    return result
