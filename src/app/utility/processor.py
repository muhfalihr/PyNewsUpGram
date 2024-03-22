from typing import *
from functools import wraps

from src.app.utility import Utilities
from src.app.other import CleverScrapper

class Processor:
    def __init__(self) -> None:
        pass

    @staticmethod
    def inewsPro(func):
        '''
        '''
        cs = CleverScrapper()
        @wraps(func)
        def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)
            
            raw_data = Utilities.raw(content=content, html=True)
            datas = cs.iNewsCS(html=raw_data)

            return datas
        return wrapper