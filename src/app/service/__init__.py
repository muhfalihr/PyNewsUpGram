from .requester import NewsSite
from .pileditor import PILEditor

class TribunNews( NewsSite ):
    def __init__( self ):
        super().__init__( "tribunnews" )

class Requester:
    def __init__( self ) -> None:
        self.tribunnews = TribunNews()