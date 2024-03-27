import json
import time
import random
import asyncio
import aiofiles

from src.app.service import Requester
from src.app.utility.processor import Processor

from datetime import datetime
from json import *

class Main:
    __process = Processor()
    def __init__(self) -> None:
        self.req = Requester()

    @__process.inewsPro
    async def iNewsReq(self, **kwargs):
        content = await self.req.inews.requester(**kwargs)
        return content
    
    @__process.kompasPro
    async def kompasReq(self, **kwargs):
        content = await self.req.kompas.requester(**kwargs)
        return content
    
    @__process.tribunNewsPro
    async def tribunNewsReq(self, **kwargs):
        content = await self.req.tribunnews.requester(**kwargs)
        return content
    
    async def resultiNews(self):
        date = datetime.now().strftime("%d-%m-%Y")
        datas = await asyncio.gather(*(self.iNewsReq(page=i, date=date) for i in range(5)))
        for i, data in enumerate(datas):
            if data["datas"]:
                await self.save(file=f"data/result-{i}.json", data=data, json=True)
    
    async def resultiTribunNews(self):
        date = datetime.now().strftime("%Y-%-m-%-d")
        datas = await asyncio.gather(*(self.tribunNewsReq(page=i, date=date) for i in range(1, 4)))
        for i, data in enumerate(datas):
            if data["datas"]:
                await self.save(file=f"data/result-{i}.json", data=data, json=True)

    async def save(self, file:str, data:str, json: bool = False):
        if json is True:
            data = dumps(data, indent=4)
        async with aiofiles.open(file, "w") as svfile:
            await svfile.write(data)

if __name__ == "__main__":
    sb = Main()
    date = datetime.now().strftime("%d-%m-%Y")
    date = datetime.now().strftime("%Y-%-m-%-d")

    # loop = asyncio.get_event_loop()
    # data = loop.run_until_complete(sb.iNewsReq(page=1, date="25-03-2024"))
    # data = asyncio.run(sb.all_req())
    # sb.main()

    asyncio.run(sb.resultiTribunNews())
    

    # full_page = 0
    # while(True):
    #     with ThreadPoolExecutor() as executor:
    #         futures = [executor.submit(sb.iNewsReq, page=i+1, date=date) for i in range(full_page, full_page + 5)]
        
    #     hasil = []

    #     for future in as_completed(futures):
    #         data = future.result()
    #         dumps = json.dumps(data, indent=4)
    #         with open(f"data/result-{random.randint(1, 100)}.json", "w") as file:
    #             file.write(dumps)

    #         hasil.append(len(data["datas"]))

    #     print(hasil)

    #     if 0 in hasil: break

    #     full_page += 5

    # full_page = 0
    # while(True):
    #     with ThreadPoolExecutor() as executor:
    #         datas = executor.map(lambda kwargs: sb.iNewsReq(**kwargs), [{'page': i + 1, 'date': date} for i in range(full_page, full_page + 5)])
        
    #     hasil = []

    #     for data in datas:
    #         dumps = json.dumps(data, indent=4)
    #         with open(f"data/result-{random.randint(1, 100)}.json", "w") as file:
    #             file.write(dumps)

    #         hasil.append(len(data["datas"]))

    #     print(hasil)

    #     if not hasil: break

    #     full_page += 5