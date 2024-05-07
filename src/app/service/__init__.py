from .requester import NewsSite
from .pileditor import PILEditor

class iNews( NewsSite ):
    def __init__( self ):
        super().__init__( "inews" )

class Detik( NewsSite ):
    def __init__( self ):
        super().__init__( "detik" )

class Kompas( NewsSite ):
    def __init__( self ):
        super().__init__( "kompas" )

class Okezone( NewsSite ):
    def __init__( self ):
        super().__init__( "okezone" )

class TribunNews( NewsSite ):
    def __init__( self ):
        super().__init__( "tribunnews" )

class Requester:
    def __init__( self ) -> None:
        self.inews = iNews()
        self.kompas = Kompas()
        self.tribunnews = TribunNews()