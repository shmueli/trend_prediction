import json

from graphs import load_graphs
from helpers import constants


start = constants.PERIODS[1]['start']
end = constants.PERIODS[4]['end']


def execute():
    calc_top_nodes(start, end, None)
    

def calc_top_nodes(start, end, num_nodes):
    output_filename = constants.RANKED_NODES_FOLDER_NAME + 'ranked_nodes'

    ranked_nodes = load_graphs.load_period_network(start, end)
    ranked_nodes = load_graphs.rank_network_nodes(ranked_nodes)
    if num_nodes!=None:
        ranked_nodes = ranked_nodes[-num_nodes:]
    print 'ranked_nodes:', len(ranked_nodes)

    json.dump(ranked_nodes, open(output_filename, 'w'))


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
