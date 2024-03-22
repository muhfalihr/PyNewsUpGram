import json
import time

from src.app.service.inews.service import iNews
from src.app.utility.processor import Processor

from datetime import datetime

class Main:
    def __init__(self) -> None:
        self.inews = iNews()

    @Processor.inewsPro
    def iNewsReq(self, **kwargs):
        resp = self.inews.requester(**kwargs)
        content = resp.content
        return content

if __name__ == "__main__":
    sb = Main()
    date = datetime.now().strftime("%d-%m-%Y")

    page = 1
    while True:
        test = sb.iNewsReq(date=date, page=page)
        nextpage = test["nextpage"]
        result = dict()
        result.update({"result": test})
        dumps = json.dumps(result, indent=4)
        
        with open(f"data/result-{page}.json", "w") as file:
            file.write(dumps)
        
        if nextpage:
            page += 1
            time.sleep(1)
        else:
            break