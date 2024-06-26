from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


class HtmlParser:
    """
    Provides a framework for parsing HTML content using different parsing libraries. 
    Offers flexibility in choosing parsing methods based on preferences or specific needs.
    """
    @staticmethod
    def bs4_parser( html: str, selector: str ):
        """
        Employs the BeautifulSoup library for parsing.
        Parses the provided HTML string using the "lxml" parser.
        Applies the specified selector to extract relevant elements.
        Handles potential exceptions and returns the parsed results.

        @params
            html: `str`
                html text
            selector: `str`
                selector
        
        @return
            result: `Beatifulsoup`
        """
        result: None = None
        try:
            html: BeautifulSoup = BeautifulSoup( html, "lxml" )
            result = html.select( selector )
        except Exception as e:
            print( e )
        finally:
            return result

    @staticmethod
    def pyq_parser( html: str, selector: str ):
        """
        Utilizes the PyQuery library for parsing.
        Processes the HTML string using PyQuery's syntax.
        Applies the selector to select desired elements.
        Manages exceptions and returns the extracted data.

        @params
            html: `str`
                html text
            selector: `str`
                selector
        
        @return
            result: `PyQuery`
        """
        result: None = None
        try:
            html: pq = pq( html )
            result = html( selector )
        except Exception as e:
            print( e )
        finally:
            return result
 