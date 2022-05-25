# Copyright 2022 British Broadcasting Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
