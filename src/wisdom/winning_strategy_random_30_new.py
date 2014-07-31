import sys
sys.path.insert(0, '../')

import winning_strategy

from helpers import constants


periods = constants.PERIODS_MONTHLY
min_in_degrees = [0]
top = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
ind = [0, 1, 2, -1]
repeats = 25
replace = [True, False]
ordering_type = 'random'
days = 30
old = False
limited_loss = True
invested_type = 'proportional'


def execute():
    winning_strategy.execute(min_in_degrees, periods, top, ind, repeats, replace, ordering_type, days, old, limited_loss, invested_type)


if __name__ == '__main__':
    execute()

    print 'Done.'
