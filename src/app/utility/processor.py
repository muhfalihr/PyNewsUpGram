from io import BytesIO
from typing import *
from functools import wraps
from PIL import Image

from src.app.utility import Utilities
from src.app.utility.parserer import CleverScrapper
from src.app.service import Requester
from src.app.service import PILEditor

class Processor:
    def __init__( self ) -> None:
        self.cs: CleverScrapper = CleverScrapper()
        self.req: Requester = Requester()
        self.pil: PILEditor = PILEditor()
        self.image: Image = Image

    def tribunNewsPro( self, func ):
        '''
        The processor retrieves data from the Tribunnews site URL
        '''
        @wraps( func )
        def wrapper( *args, **kwargs ):
            content: Any = func( *args, **kwargs )
            content: str = Utilities.raw( content=content, html=True )

            URLLIST: List[ str ] = self.cs.tribunNewsLL( html=content )

            @self.byteContentPhoto
            def image_processing(**kwargs):
                resp = self.req.tribunnews.request_taking_byte(**kwargs)
                return resp

            for content, url in self.req.tribunnews.second_requester( list_url=URLLIST, timeout=120, condition=b'id="article"' ):
                data: dict = self.cs.tribunNewsCS( html=content, url=url )

                if ( data[ "title" ] ):
                    detail_img = image_processing( url=data[ "thumbnail" ] )
                    with self.image.open( fp=detail_img[ 0 ] ) as im:
                        im = self.pil.crop_to_square( im )
                        im = self.pil.scale( im )
                        im = self.pil.add_title( im=im, text=data[ "title" ] )
                        im = self.pil.add_watermark( im )
                        im = self.pil.saved( im=im, path=f"./image/{ detail_img[ 2 ] }" )
            
            print( kwargs )
        return wrapper
    
    def byteContentPhoto( self, func ):
        '''
        '''
        @wraps( func )
        def wrapper( *args, **kwargs ):
            response: Tuple = func( *args, **kwargs )
            data: bytes = BytesIO(response[0])
            content_type: str = response[1].get("Content-Type")
            filename: str = Utilities.takeFilename(response[2])
            return ( data, content_type, filename )
        return wrapper