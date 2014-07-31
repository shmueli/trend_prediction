import sys
sys.path.insert(0, '../')

import json

from helpers import constants


_ranked_nodes = None


def load():
    global _ranked_nodes

    if _ranked_nodes!=None:
        return

    input_filename = constants.RANKED_NODES_FOLDER_NAME + 'ranked_nodes'
    
    _ranked_nodes = json.load(open(input_filename, 'r'))


def get_ranked_nodes():
    load()

    return _ranked_nodes
