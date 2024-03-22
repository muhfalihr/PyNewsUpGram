import re
import os
import json
import hashlib

from typing import *

class Utilities:
    def __init__(self) -> Any:
        pass

    @staticmethod
    def raw(content: str | bytes, html: bool = False) -> Dict[Any, Any] | str:
        '''
        Convert API response to JSON.

        Arguments:
          - content (required): response content (str | bytes)
        '''
        raw_data = None

        if html == False:
          resp_content: str = content.decode("utf-8")
          raw_data: Dict[Any] = json.loads(resp_content)
        else:
          raw_data: str = content.decode("utf-8")

        return raw_data
    
    @staticmethod
    def mkdirNotExist(name: str) -> None:
        '''
        Creates a folder if the folder does not already exist in the current directory.

        Arguments:
          - name (required): the name of the new folder to be created. (str)
        '''
        pathdir = os.getcwd()

        if name not in os.listdir(path=pathdir):
            path = os.path.join(pathdir, name)
            os.mkdir(path=path)
    
    @staticmethod
    def hashTomd5(string: str) -> str:
        '''
        Hashing the string to md5

        Arguments :
          - string (reqired)
        '''
        hash_md5 = hashlib.md5()
        hash_md5.update(string.encode("utf=8"))
        return hash_md5.hexdigest()
    
    @staticmethod
    def webName(string: str):
        '''
        Retrieves the wen name from a URL string

        Arguments :
          - string (required)
        '''
        web_name = re.match(pattern=r'https?://(www\.)?([^/]+)', string=string)
        if web_name: web_name = web_name.group(2)
        return web_name