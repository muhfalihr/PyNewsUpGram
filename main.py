from src.app.service import Requester
from src.app.utility.processor import Processor
from src.app.service.pileditor import PILEditor

from datetime import datetime
from PIL import Image
from json import *

class Main:
    __process = Processor()
    def __init__(self) -> None:
        self.req = Requester()
        self.pil = PILEditor()

    @__process.byteContentPhoto
    def image(self, **kwargs):
        response = self.req.tribunnews.request_taking_byte(**kwargs)
        return response
    
    @__process.tribunNewsPro
    def tribunNewsReq(self, **kwargs):
        content = self.req.tribunnews.requester(**kwargs)
        return content

    def resultiTribunNews(self):
        date = datetime.now().strftime("%Y-%-m-%-d")
        for i in range(5):
            self.tribunNewsReq(page=i, date=date)

    def save(self, file: str, data: str, json: bool = False):
        if json is True:
            data = dumps(data, indent=4)
        with open(file, "w") as svfile:
            svfile.write(data)

if __name__ == "__main__":
    sb = Main()
    sb.resultiTribunNews()