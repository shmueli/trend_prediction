import sys
sys.path.insert(0, '../')

from helpers import constants

import json


def load(varname):
    input_filename = constants.DYNAMICS_FOLDER_NAME + 'etoro_' + varname
    
    data = json.load(open(input_filename, 'r'))
    
    return data
