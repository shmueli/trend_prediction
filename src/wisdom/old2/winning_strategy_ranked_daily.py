# random nodes - [today, tomorrow) - with net replace

import sys
sys.path.insert(0, '../')

from wisdom import winning_strategy_ranked_period

from helpers import constants


min_in_degrees = [0]
top = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
ind = [0, 1, 2, -1]
repeats = 1
replace = [True, False]
ordering_type = 'ranked'
returns_type = 'daily'


def execute():
    for min_in_degree in min_in_degrees:
        for p in constants.PERIODS_MONTHLY:
            winning_strategy_ranked_period.store_daily_returns_for_all_individuals(constants.PERIODS_MONTHLY, p, min_in_degree, top, ind, repeats, replace, ordering_type, returns_type)


#####################################################################################
# ## main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
