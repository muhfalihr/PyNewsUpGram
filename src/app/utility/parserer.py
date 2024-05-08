import re
import json

from src.app.library.libparser import HtmlParser
from src.app.utility.utility import Utilities

from typing import *
from datetime import datetime
from googletrans import Translator

class CleverScrapper:
    def __init__( self ) -> None:
        
        self.parser: HtmlParser = HtmlParser()
        self.translate: Translator = Translator()
        self.next: bool = False

    def tribunNewsLL( self, **kwargs ):
        '''Gets the URLs from the HTML response and 
        returns a list containing values in the form of article URLs.

        @params
            html: `str`
                response content decoded to string
        
        @return
            URLIST: `List[ str ]`
                Url List
        '''
        RAW_DATA: str = kwargs.get( "html" )
        
        DIV = self.parser.pyq_parser( html=RAW_DATA, selector='div[class="main"] div[class="content"] div[class="fl w677"] div[class="bsh ovh"] div[class="p2030"]' )

        URLIST: List[ str ] = [
            url.attr( "href" ) + "?page=all"
            for url in self.parser.pyq_parser( html=DIV, selector='div[class="pt10 pb10"] ul[class="lsi"]' ).find( 'li[class="ptb15"] h3[class="f16 fbo"] a' ).items()
        ]
        return URLIST
    
    def tribunNewsCS( self, **kwargs ):
        '''Take the necessary data.

        @params
            html: `str`
                response content decoded to string
            url: `str`
                URL of the site from which the data will be retrieved
        
        @return
            data: `Dict[ Any ]`
        '''
        data: dict = dict()
        RAW_DATA, URL = kwargs.get( "html" ), kwargs.get( "url" )

        ID: str = Utilities.hashTomd5( string=URL )
        SOURCE: str|Any|None = Utilities.webName( string=URL )

        DIV = self.parser.pyq_parser( html=RAW_DATA, selector='div[class="main"] div[class="content"] div[class="fl w677"] div[class="bsh mb20"] div[id="article"]' )

        JSON_DATA: str = self.parser.pyq_parser( html=RAW_DATA, selector='script[type="application/ld+json"]' ).eq( 1 ).text()
        JSON_DATA: Dict[ str ] = json.loads( JSON_DATA ) if JSON_DATA else { "datePublished": datetime.now().strftime( "%Y-%m-%dT%H:%M:%S+07:00" ), "image": None }

        JUDUL = self.parser.pyq_parser( html=DIV, selector='h1[id="arttitle"]' ).text()
        AUTHOR_NAME = self.parser.pyq_parser( html=DIV, selector='div[class="mt10"] div[class="f20 credit mt10"] h6 div[id="penulis"] a ').text()
        AUTHOR_LINK = self.parser.pyq_parser( html=DIV, selector='div[class="mt10"] div[class="f20 credit mt10"] h6 div[id="penulis"] a' ).attr( "href" )
        EDITOR = self.parser.pyq_parser( html=DIV, selector='div[class="mt10"] div[class="f20 credit mt10"] h6 div[id="editor"] a' ).text()
        EDITOR_LINK = self.parser.pyq_parser( html=DIV, selector='div[class="mt10"] div[class="f20 credit mt10"] h6 div[id="editor"] a' ).attr( "href" )
        THUMBNAIL = self.parser.pyq_parser( html=DIV, selector='div[id="article_con"] div[id="artimg"] div[class="pb20 ovh"] div[class="ovh imgfull_div"] a[class="glightbox"] img' ).attr( "src" )
        THUMBNAIL_CAPTION = self.parser.pyq_parser( html=DIV, selector='div[id="article_con"] div[id="artimg"] div[class="pb20 ovh"] div[class="arial f12 pt5 grey2"]' ).text()
        
        BODY_TEXT = self.parser.pyq_parser( html=DIV, selector='div[id="article_con"] div[class="side-article txt-article multi-fontsize"]' )
        BODY_TEXT: str = re.sub( pattern=r'<p class="baca">.*?</p>', repl='', string=BODY_TEXT.__str__() )
        RAW_CONTENT = self.parser.pyq_parser( html=BODY_TEXT, selector='p' ).text() if ( BODY_TEXT ) else ''
        CONTENT: str = re.sub( pattern=r'^(\b[A-Z]+[\.]*[A-Z]+[\s]*-{1,2}[\s]*\b|\b[A-Z]+[\.]*[A-Z]+\b[,]*\s\b[A-Z]+[\s]*-[\s]*\b|Laporan\sWartawan\sTribunnews[\.com]{0,1}.+\b[A-Z]+[\.]*[A-Z]+\b[,]*\s\b[A-Z]+[\s]*-{1,2}[\s]*\b)', repl='', string=RAW_CONTENT, flags=re.DOTALL )

        PUBLISH_DATE = datetime.strptime( JSON_DATA.get( "datePublished" ), "%Y-%m-%dT%H:%M:%S+07:00" ).strftime( "%Y-%m-%d %H:%M:%S" )
        
        TAGS = [
            tag.text()
            for tag in self.parser.pyq_parser( html=DIV, selector='div[id="article_con"] div[class="side-article mb5"] div[class="mb10 f16 ln24 mb10 mt5"]' ).find( 'h5[class="tagcloud3"] a' ).items()
        ]
        if ( not THUMBNAIL ): THUMBNAIL: str|None = JSON_DATA.get( "image" )
        DESC = CONTENT[ :100 ] + "..." if ( CONTENT ) else ""
        
        data.update({
            "id": ID,
            "link": URL,
            "source": SOURCE,
            "title": JUDUL,
            "author_name": AUTHOR_NAME,
            "author_link": AUTHOR_LINK,
            "publish_date": PUBLISH_DATE,
            "thumbnail": THUMBNAIL,
            "thumbnail_caption": THUMBNAIL_CAPTION,
            "content": CONTENT,
            "description": DESC,
            "editor_name": EDITOR,
            "editor_link": EDITOR_LINK,
            "tags": TAGS
        })
        return data