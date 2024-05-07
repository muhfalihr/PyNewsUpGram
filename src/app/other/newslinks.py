from typing import *

class NewsLinks:
    def __init__( self ) -> AnyStr:
        self.TRIBUNNEWS: str = "https://www.tribunnews.com/index-news?date={date}&page={page}"
    
    def newslink( self, sitename: str ) -> str|None:
        '''
        Collection of links used.

        Arguments :
          - sitename ( str ) : Site name. Ex. :mod:`tribunnews`
        '''
        newslink: None = None
        
        if sitename == "tribunnews":
            newslink: str = self.TRIBUNNEWS
        return newslink