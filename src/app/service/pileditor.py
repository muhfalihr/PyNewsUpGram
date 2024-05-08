import os
import configparser

from typing import *
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFilter, ImageFont


class PILEditor:
    load_dotenv(dotenv_path="./.env")
    def __init__( self ) -> Image.Image:
        
        self.config = configparser.ConfigParser()
        self.env = os.getenv( "PYNEWS_CONFIG" )
        self.image_draw = lambda im: ImageDraw.Draw( im )
        self.image_font_true_type = lambda **kwargs: ImageFont.truetype( **kwargs )
        self.image_filter = ImageFilter

        self.config.read( self.env )

    @property
    def config_dict(self) -> dict:
        '''Retrieving values from configurations taken from the config file.
        This is used to complete the requirements of this code,
        without hardcoding it, so that it looks cleaner.
        '''
        config = self.config.__dict__.get( "_sections", {} ).get( "pil_editor", {} )
        value = config.get( "square_pixel", 0 )
        if isinstance( value, (int, str) ):
            config[ "square_pixel" ] = int( value )
        else:
            raise Notletters( f"The value of the 'square_pixel' parameter must be of `{ int.__name__ }`" )
        return config
    
    @property
    def square_px(self): return self.config_dict.get( "square_pixel" )

    @property
    def field_color(self): return self.config_dict.get( "field_color", "" )

    @property
    def text_color(self): return self.config_dict.get( "text_color", "" )

    @property
    def watermark_title(self): return self.config_dict.get( "watermark_title", "" )

    @property
    def title_font(self): return self.config_dict.get( "title_font", "" )

    @property
    def watermark_font(self): return self.config_dict.get( "watermark_font", "" )

    def scale( self, im: Image.Image ) -> Image.Image:
        '''Scales the size of the image to match the size specified in the config file.
        This is only used for square field sizes.
        If it is anything other than square then there will be a problem in this code.
        @params
            im: :mod:`Image.Image`
                obj image
        
        @return
            im: :mod:`Image.Image`
                obj image
        '''
        width, height = ( self.square_px / im.width ), ( self.square_px / im.height )
        return im.resize( ( round( im.width * width ), round( im.height * height ) ) )
    
    def crop_to_square( self, im: Image.Image ) -> Image.Image:
        '''Crop the image into a square shape.
        @params
            im: :mod:`Image.Image`
                obj image
        
        @return
            cropped_image: :mod:`Image.Image`
                obj image
        '''
        box_calc = lambda width, height, min_dimension, divnum: (
            ( width - min_dimension ) / divnum,
            ( height - min_dimension ) / divnum,
            ( width + min_dimension ) / divnum,
            ( height + min_dimension ) / divnum
        )
        width, height = im.size
        min_dimension = min( width, height )
        box = box_calc( width=width, height=height, min_dimension=min_dimension, divnum=2 )
        cropped_image = im.crop( box )
        return cropped_image
    
    def rounded_rectangle( self, im: Image.Image, num ) -> Image.Image:
        '''Create a rounded rectangle shape.
        Used for the background of the title text.
        @params
            im: :mod:`Image.Image`
                obj image
        
        @return
            im: :mod:`Image.Image`
                obj image
        '''
        size = im.size
        draw = self.image_draw( im )

        box_calc = lambda size: ( 
            ( 
                ( size[0] * 0.021 ), ( size[1] * ( 1.0 - num ) ) 
            ),
            ( 
                ( size[0] - ( size[0] * 0.021 ) ), ( size[1] - ( size[0] * 0.021 ) ) 
            )
        )
        
        draw.rounded_rectangle( box_calc( size=size ), fill=self.field_color, width=10, radius=10 )
        return im

    def wrap_text( self, text: str, font: ImageFont.FreeTypeFont, max_width: int ) -> List[ str ]:
        '''Wrap text base on specified width. 
        This is to enable text of width more than the image width to be display
        nicely.
        @params:
            text: :mod:`str`
                text to wrap
            font: :mod:`ImageFont.FreeTypeFont`
                font of the text
            max_width: :mod:`int`
                width to split the text with
        @return
            lines: :mod:`list[str]`
                list of sub-strings
        '''
        lines = []
        
        if ( font.getbbox( text )[ 2 ] <= max_width ):
            lines.append( text )
        else:
            words = text.split(' ')
            i = 0

            while ( i < len( words ) ):
                line = ''
                while ( i < len( words ) ) and ( font.getbbox( line + words[ i ] )[ 2 ] <= max_width ):
                    line = ( line + words[ i ] + " " )
                    i += 1
                if ( not line ):
                    line = words[ i ]
                    i += 1
                lines.append(line)
        return lines, len( lines )
    
    def height_calc( self, num: float, txtsize: float ) -> float:
        '''
        '''
        addition = 0.5 if num == 3 else 1.0 if num < 3 else 0
        num = ( num + addition )
        num = ( ( num / 10.0 ) + ( ( txtsize / 1000.0 ) * num ) )
        return num

    def add_title( self, im: Image.Image, text: str ) -> Image.Image:
        '''Add a title to the image.
        @params
            im: :mod:`Image.Image`
                obj image
            text: :mod:`str`
        
        @return
            im: :mod:`Image.Image`
                obj image
        '''
        size = im.size
        draw = self.image_draw( im )
        font = self.image_font_true_type( font=self.title_font, size=65 )

        txt_size = font.getbbox( text )
        lines, length_line = self.wrap_text( text=text, font=font, max_width=( im.width * 0.9 ) )

        num = self.height_calc( length_line, txt_size[1] )
        x, y = ( size[ 0 ] * 0.042 ), ( size[ 1 ] * ( 1.0 - num + 0.021 ) )

        im = self.rounded_rectangle( im, num )
        asc, desc = font.getmetrics()
        for line in lines:
            draw.text( ( x, y ), text=line, font=font, fill=self.text_color, anchor="la" )
            y += ( asc + desc )
        return im
    
    def add_watermark( self, im: Image.Image ) -> Image.Image:
        '''Add a watermark to the image.
        @params
            im: :mod:`Image.Image`
                obj image

        @return
            im: :mod:`Image.Image`
                obj image
        '''
        size = im.size
        draw = self.image_draw( im )
        x, y = ( size[ 0 ] * 0.958 ), ( size[ 1 ] * 0.896 )
        font = self.image_font_true_type( font=self.watermark_font, size=65 )
        draw.text(
            ( x, y ), 
            text=self.watermark_title, fill=self.text_color, 
            font=font, anchor="ra", stroke_width=2, stroke_fill="black"
        )
        return im
    
    def smoothing_image( self, im: Image.Image ) -> Image.Image:
        '''Sharpens the image to be smooth and detailed.
        @params
            im: :mod:`Image.Image`
                obj image

        @return
            im: :mod:`Image.Image`
                obj image
        '''
        smooth_and_detail = im.filter( self.image_filter.SMOOTH ).filter( self.image_filter.DETAIL )
        return smooth_and_detail

    def saved( self, im: Image.Image, path: str ) -> Image.Image:
        '''Save the image to an internal path.
        @params
            im: :mod:`Image.Image`
                obj image

        @return
            im: :mod:`Image.Image`
                obj image
        '''
        im.save(path)

class Notletters( Exception ): pass