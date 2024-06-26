import re
import os
import json
import hashlib

from typing import *
from googletrans import Translator

class Utilities:
    def __init__(self) -> Any:
        pass

    @staticmethod
    def raw( content: str | bytes, html: bool = False ) -> Dict[ Any, Any ] | str:
        '''Convert API response to JSON.

        @params
            content: `str | bytes`
                    response content
            html: `bool`
                    is it html ? (Optional). Default `False`

        @return
            raw_data: `str`
                    raw html or dictionary response
        '''
        raw_data = None

        if ( html == False ):
          resp_content: str = content.decode( "utf-8" )
          raw_data: Dict[ Any ] = json.loads( resp_content )
        else:
          raw_data: str = content.decode( "utf-8" )

        return raw_data
    
    @staticmethod
    def mkdirNotExist(name: str) -> None:
        '''Creates a folder if the folder does not already exist in the current directory.

        @params
            name: `str`
                    the name of the new folder to be created
        
        @return
            >>> return os.mkdir( path=path )
        '''
        pathdir = os.getcwd()

        if ( name not in os.listdir( path=pathdir ) ):
            path = os.path.join( pathdir, name )
            os.mkdir( path=path )
    
    @staticmethod
    def hashTomd5( string: str ) -> str:
        '''Hashing the string to md5

        @params
            string: `str`
                    text string to be hashed
        
        @return
            >>> return hash_md5.hexdigest()
        '''
        hash_md5 = hashlib.md5()
        hash_md5.update( string.encode( "utf=8" ) )
        return hash_md5.hexdigest()
    
    @staticmethod
    def webName( string: str ):
        '''Retrieves the wen name from a URL string

        @params
            string: `str`
                    the url from which the web name will be retrieved
        
        @return
            web_name: `Match[ str | None ]`
                    web name
        '''
        web_name: Match[ str | None ] = re.match( pattern=r'https?://(www\.)?([^/]+)', string=string )
        if web_name: web_name: Match[ str | None ] = web_name.group( 2 )
        return web_name

    @staticmethod
    def takeFilename( url: str ):
        '''Retrieves file name from url using regex.

        @params
            url: `str`
                    the url from which the file name will be retrieved
        
        @return
            filename: `Match[ str | None ]`
                    file name
        '''
        pattern = re.compile( pattern=r'([^/]+)\.(jpg|mp4)$' )
        matches = pattern.search( string=url )
        if matches: filename = matches.group( 0 )
        return filename