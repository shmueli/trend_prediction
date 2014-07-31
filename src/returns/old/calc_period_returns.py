import sys
sys.path.insert(0, '../')

from datetime import datetime, timedelta
import json

import calc_daily_returns
from graphs import load_graphs
from helpers import constants


def execute():
    for p in constants.PERIODS:
        store_period_returns_for_all_individuals(constants.PERIODS[p]['start'], constants.PERIODS[p]['end'], p)


def store_period_returns_for_all_individuals(start, end, period):
    output_filename = constants.RETURNS_FOLDER_NAME + 'period_returns' + '_' + str(period)
    
    returns = {}
    
    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT) 

        g_trades = load_graphs.load_time_network(time, data=True)

        for v in g_trades.node:
            r = calc_daily_returns.calc_returns_for_individual(g_trades, v, time, end, period)
            
            if v not in returns:
                returns[v] = {}                    
            returns[v][time_str] = r
             
        time = time + timedelta(days=1)
        
    json.dump(returns, open(output_filename, 'w'))


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
