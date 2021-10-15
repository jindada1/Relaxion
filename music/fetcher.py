'''
on  :  2019-07-11
by  :  Kris Huang

for : request data from other platforms
'''

from aiohttp import ClientSession
from datetime import datetime
import time
import json
import base64
import urllib

class Fetcher(object):

    def __init__(self, **kwargs):

        self.cookies = {}
        self.headers = {}

    async def _asyncGetHeaders(self, url, params = None):
        async with ClientSession() as session:
            resp = await session.get(url, params=params)
            await session.close()
            return resp.headers

    async def _asyncGetText(self, url, params = None):
        async with ClientSession() as session:
            resp = await session.get(url, params=params)
            txt = await resp.text()
            await session.close()
            return txt


    async def _asyncGetJson(self, url, params = None):
        async with ClientSession() as session:
            resp = await session.get(url, params=params)
            js = json.loads(await resp.text())
            await session.close()
            return js


    async def _asyncPostJson(self, url, params = None, cookies = None):
        async with ClientSession(cookies = cookies) as session:
            resp = await session.post(url, data=params, headers=self.headers)
            js = json.loads(await resp.text())
            await session.close()
            return js


    async def _asyncGetJsonHeaders(self, url, params = None):
        async with ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as resp:
                js = json.loads(await resp.text())
                await session.close()
                return js


    async def _asyncGetJsonHeadersCookies(self, url, params = None):
        async with ClientSession(cookies=self.cookies) as session:
            async with session.get(url, params=params, headers=self.headers) as resp:
                js = json.loads(await resp.text())
                await session.close()
                return js

    async def _asyncGetTextHeadersCookies(self, url, params = None):
        async with ClientSession(cookies=self.cookies) as session:
            async with session.get(url, params=params, headers=self.headers) as resp:
                txt = await resp.text()
                await session.close()
                return txt


    def jsonify(self, _dict):

        return json.dumps(_dict).replace(" ", '')

    def base64decode(self, text):
        
        return base64.b64decode(text).decode(encoding="utf-8-sig")

    def base64encode(self, text):

        return base64.b64encode(text)

    def to_time(self, timestamp):
        
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d, %H:%M:%S")

    @property
    def now_str(self):

        return str(int(time.time()))

    def quote_cna(self, val):
        if '%' in val:
            return val
        return urllib.parse.quote(val)

    def split_url(self, url):

        return urllib.parse.urlsplit(url)

    def unsplit_url(self, url):

        return urllib.parse.urlunsplit(url)
    