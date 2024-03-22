import re
import os
import logging

# from src.app.library import setup_logging

from requests.sessions import Session
from faker import Faker
from dotenv import dotenv_values
from typing import *

class iNews:

    __dotenv_path = os.path.join("src", "env", "inews", ".env")
    __config = dotenv_values(dotenv_path=__dotenv_path)
    
    def __init__(self) -> None:
        """
        ...
        """
        self.faker = Faker()
        self.session = Session()

        self.headers = dict()
        self.headers["Accept"] = iNews.__config.get("ACCEPT")
        self.headers["Accept-Encoding"] = iNews.__config.get("ACCEPTENCOD")
        self.headers["Accept-Language"] = iNews.__config.get("ACCEPTLANG")
        self.headers["Cookie"] = iNews.__config.get("COOKIE")
        self.headers["Sec-Ch-Ua"] = iNews.__config.get("SEC_CH_UA")
        self.headers["Sec-Ch-Ua-Platform"] = iNews.__config.get("SEC_CH_UA_PLATFORM")
        self.headers["Sec-Fetch-Dest"] = iNews.__config.get("SEC_FETCH_DEST")
        self.headers["Sec-Fetch-Site"] = iNews.__config.get("SEC_FETCH_SITE")
        self.headers["User-Agent"] = self.faker.user_agent()

        # setup_logging()
        # self.logger = logging.getLogger(self.__class__.__name__)

    def requester(self, **kwargs):
        """
        ...
        """
        if "url" not in kwargs.keys():
            DATE = kwargs.get("date", None)
            PAGE = kwargs.get("page", None)
            kwargs.update({"url": f"https://www.inews.id/indeks/news/{DATE}/{PAGE}"})
            kwargs.update({"method": "GET"})
            kwargs.update({"timeout": 60})
            
            del kwargs["date"]
            del kwargs["page"]

        kwargs.update({"headers": self.headers})
        
        RESP = self.session.request(**kwargs)
        
        if RESP.status_code == 200:
            return RESP
        else:
            raise f"Error! status code {RESP.status_code} : {RESP.reason}"

if __name__ == "__main__":
    cek = iNews()