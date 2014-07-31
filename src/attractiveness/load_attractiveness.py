import sys
sys.path.insert(0, '../')

import json

from helpers import constants


def load(varname):
    pos = json.load(open(constants.ATTRACTIVENESS_FOLDER_NAME + varname, 'r'))
    
    return pos
