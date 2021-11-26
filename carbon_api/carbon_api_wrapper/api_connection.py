import aiohttp
from urllib.parse import urljoin


class ApiConnection:
    def __init__(self, base):
        self.base_url = base

    async def status(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), trust_env=True) as session:
            async with session.get(self.base_url) as r:
                return r.status

    async def get(self, endpoint):
        url = urljoin(self.base_url, endpoint)
        # issue with ssl certs overridden by ssl=false
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), trust_env=True) as session:
            async with session.get(url) as r:
                json = await r.json()
                if r.status != 200:
                    print(f"Error requesting: {url} Status code: {r.status}")
                return json
