import os
import time
import logging

from src.app.library import setup_logging
from src.app.other.newslinks import NewsLinks

from requests.sessions import Session
from faker import Faker
from dotenv import dotenv_values
from typing import *

class ErrorRequests( Exception ): pass

class NewsSite:
    def __init__( self, site_name: str ) -> Any:

        self.session: Session = Session()
        self.newslinks: NewsLinks = NewsLinks()

        self.dotenv_path: str = os.path.join( "src", "env", site_name.lower(), ".env" )
        self.config: Dict[ str, str|None ] = dotenv_values( dotenv_path=self.dotenv_path )
        self.sitename = site_name

    def request_headers( self ):
        '''
        Creation of requests headers
        '''
        self.faker: Faker = Faker()

        self.headers: dict = dict()
        self.headers[ "Accept" ] = self.config.get( "ACCEPT" )
        self.headers[ "Accept-Encoding" ] = self.config.get( "ACCEPTENCOD" )
        self.headers[ "Accept-Language" ] = self.config.get( "ACCEPTLANG" )
        self.headers[ "Cookie" ] = self.config.get( "COOKIE" )
        self.headers[ "Sec-Ch-Ua" ] = self.config.get( "SEC_CH_UA" )
        self.headers[ "Sec-Ch-Ua-Platform" ] = self.config.get( "SEC_CH_UA_PLATFORM" )
        self.headers[ "Sec-Fetch-Dest" ] = self.config.get( "SEC_FETCH_DEST" )
        self.headers[ "Sec-Fetch-Site" ] = self.config.get( "SEC_FETCH_SITE" )
        self.headers[ "User-Agent" ] = self.faker.user_agent()
        return self.headers
    
    def requester( self, **kwargs ):
        '''
        '''
        if "url" not in kwargs: (
            kwargs.update({
                "url": self.newslinks.newslink( sitename=self.sitename ).format( date=kwargs.pop( "date" ), page=kwargs.pop( "page" ) ),
                "timeout": 240
            })
        )
        kwargs.update( { "method": "GET" ,"headers": self.request_headers() } )

        response = self.session.request( **kwargs )
        if ( response.status_code == 200 ): return response.content
        else: raise ErrorRequests( f"Error! status code { response.status_code } : { response.reason }" )

    def second_requester( self, **kwargs ):
        '''
        '''
        LISTURL: List[ str ] = kwargs.pop( "list_url" )
        CONDITION: bytes = kwargs.pop( "condition" ) if ( "condition" in kwargs ) else None

        for url in LISTURL:
            response_content: None = None
            kwargs.update( { "url": url, "headers": self.request_headers() } )
            
            while ( True ):
                time.sleep( 0.5 )
                response_content: bytes = self.requester( **kwargs )
                if ( CONDITION in response_content ): break
            yield response_content, url
    
    def request_taking_byte( self, **kwargs ):
        '''
        '''
        kwargs.update( { "method": "GET", "timeout": 240, "url": kwargs.get("url"), "headers": self.request_headers() } )
        response = self.session.request( **kwargs )
        if ( response.status_code == 200 ): return ( response.content, response.headers, kwargs.get( "url" ) )
        else: raise ErrorRequests( f"Error! status code { response.status_code } : { response.reason }" )
