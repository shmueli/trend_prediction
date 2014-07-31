import sys
sys.path.insert(0, '../')

import json

from helpers import constants

import sets


_instruments = None


def load():
    global _instruments

    if _instruments!=None:
        return _instruments

    input_filename = constants.RATES_FOLDER_NAME + 'instruments'
    
    _instruments = sets.Set( json.load(open(input_filename, 'r')) )
    
    return _instruments
