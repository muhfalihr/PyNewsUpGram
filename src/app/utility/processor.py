import asyncio

from typing import *
from functools import wraps

from src.app.utility import Utilities
from src.app.utility.parserer import CleverScrapper
from src.app.service import Requester

class Processor:
    def __init__(self) -> None:
        self.cs = CleverScrapper()
        self.req = Requester()

    def inewsPro(self, func):
        '''
        '''
        @wraps(func)
        async def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)
            
            URLLIST, NEXTPAGE = self.cs.iNewsLL(html=await content)

            DATAS = []

            async for content, url in self.req.inews.second_requester(list_url=URLLIST, timeout=120):
                data = self.cs.iNewsCS(html=content, url=url)
                DATAS.append(data)
            
            RESULT = {
                "datas": DATAS,
                "nextpage": NEXTPAGE
            }
            return RESULT
        return wrapper
    
    def kompasPro(self, func):
        '''
        '''
        @wraps(func)
        async def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)

            URLLIST = self.cs.kompasLL(html=await content)
            print(URLLIST)
            return URLLIST
        return wrapper
    
    def tribunNewsPro(self, func):
        '''
        '''
        @wraps(func)
        async def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)

            URLLIST = self.cs.tribunNewsLL(html=await content)

            DATAS = []

            async for content, url in self.req.tribunnews.second_requester(list_url=URLLIST, timeout=120):
                await asyncio.sleep(0.3)
                data = self.cs.tribunNewsCS(html=content, url=url)
                DATAS.append(data)
            
            RESULT = {
                "datas": DATAS
            }
            print(kwargs)
            return RESULT
        return wrapper