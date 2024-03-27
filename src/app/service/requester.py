import re
import os
import logging
import aiofiles
import asyncio

# from src.app.library import setup_logging
from src.app.other.newslinks import NewsLinks

from aiohttp import ClientSession, ClientResponseError
from requests.sessions import Session
from faker import Faker
from dotenv import dotenv_values
from typing import *

class NewsSite:
    def __init__(self, site_name: str):

        self.newslinks = NewsLinks()

        dotenv_path = os.path.join("src", "env", site_name.lower(), ".env")
        self.config = dotenv_values(dotenv_path=dotenv_path)
        self.sitename = site_name

    def set_config(self):
        self.faker = Faker()
        self.session = Session()

        self.headers = dict()
        self.headers["Accept"] = self.config.get("ACCEPT")
        self.headers["Accept-Encoding"] = self.config.get("ACCEPTENCOD")
        self.headers["Accept-Language"] = self.config.get("ACCEPTLANG")
        self.headers["Cookie"] = self.config.get("COOKIE")
        self.headers["Sec-Ch-Ua"] = self.config.get("SEC_CH_UA")
        self.headers["Sec-Ch-Ua-Platform"] = self.config.get("SEC_CH_UA_PLATFORM")
        self.headers["Sec-Fetch-Dest"] = self.config.get("SEC_FETCH_DEST")
        self.headers["Sec-Fetch-Site"] = self.config.get("SEC_FETCH_SITE")
        self.headers["User-Agent"] = self.faker.user_agent()
        return self.headers
    
    async def requester(self, **kwargs):
        '''
        '''
        if "url" not in kwargs: (
            kwargs.update({
                "url": self.newslinks.newslink(sitename=self.sitename).format(date=kwargs.pop("date"), page=kwargs.pop("page")),
                "timeout": 240
            })
        )
        kwargs.update({"headers": self.set_config()})

        async with ClientSession() as session:
            await asyncio.sleep(0.3)
            async with session.get(**kwargs) as response:
                if response.status == 200:
                    return await response.text()
                else: raise ClientResponseError(f"Error! status code {response.status} : {response.reason}")

    async def second_requester(self, **kwargs):
        '''
        '''
        LISTURL = kwargs.pop("list_url")
        for url in LISTURL:
            if "/multimedia/video/" in url: continue

            kwargs.update({"url": url, "headers": self.set_config()})
            
            response = await self.requester(**kwargs)
            yield response, url