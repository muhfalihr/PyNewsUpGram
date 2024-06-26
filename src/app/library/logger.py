import os
import yaml
import logging.config

from src.app.utility import Utilities
from configparser import ConfigParser
from typing import *

def setup_logging( default_path="logging.yaml", default_level=logging.INFO, env_key="LOG_CFG", log_section=None ):
    """Setup logging configuration

    @params
        default_path: `str`
            Default path for configuration log `logging.yaml`
        default_level: `logging.INFO`
        env_key: `str`
            Default environment key `LOG_CFG`
        log_section: `Any|None`
    
    @return
        >>>     logging.config.dictConfig( config )
        >>> else:
        >>>     logging.basicConfig( level=default_level )
    """
    path: str = default_path
    value: str | None = os.getenv( env_key, None )
    configparser: ConfigParser = ConfigParser()
    configparser.read( "config.ini" )
    
    if value: path: str = value
    if os.path.exists( path ):
        
        with open( path, "rt" ) as f:
            config: Any = yaml.safe_load( f.read() )
            
            if log_section:

                Utilities.mkdirNotExist( name="log" )
                
                if configparser.getboolean( "log", "sectionable" ):
                    filepath: str = os.path.join( configparser.get( "log", "path" ), log_section )
                
                else:
                    filepath: str = os.path.join( configparser.get( "log", "path" ) )
                
                if not os.path.exists( filepath ):
                    os.makedirs( filepath )

                info_file_name: str = "%s/%s" % ( filepath, config[ "handlers" ][ "info_file_handler" ][ "filename" ], )
                error_file_name: str = "%s/%s" % ( filepath, config[ "handlers" ][ "error_file_handler" ][ "filename" ], )
                debug_file_name: str = "%s/%s" % ( filepath, config[ "handlers" ][ "debug_file_handler" ][ "filename" ], )

                config.get( "handlers", {} ).get( "info_file_handler", {} )[ "filename" ] = info_file_name
                config.get( "handlers", {} ).get( "error_file_handler", {} )[ "filename" ] = error_file_name
                config.get( "handlers", {} ).get( "debug_file_handler", {} )[ "filename" ] = debug_file_name

        logging.config.dictConfig( config )
    else:
        logging.basicConfig( level=default_level )