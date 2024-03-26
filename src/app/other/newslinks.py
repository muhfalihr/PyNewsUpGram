from typing import *

class NewsLinks:
    def __init__(self) -> AnyStr:
        self.INEWS = "https://www.inews.id/indeks/news/{date}/{page}"
        self.KOMPAS = "https://indeks.kompas.com/?site=news&date={date}&page={page}"
        self.TRIBUNNEWS = "https://www.tribunnews.com/index-news?date={date}&page={page}"
    
    def newslink(self, sitename: str):
        '''
        '''
        newslink = None
        
        if sitename == "inews":
            newslink = self.INEWS
        elif sitename == "kompas":
            newslink = self.KOMPAS
        elif sitename == "tribunnews":
            newslink = self.TRIBUNNEWS
        return newslink