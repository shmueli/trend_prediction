import sys
sys.path.insert(0, '../')

import visualize

from helpers import constants


periods = constants.PERIODS_MONTHLY
unified = 6
min_in_degrees = [0]
top = [str(t_int) for t_int in [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]]
ind = [str(i_int) for i_int in [0, 1, 2, -1]]
repeats = [str(j_int) for j_int in range(25)]
replace = ['true', 'false']
ordering_type = 'random'
days = 30
old = False


def execute():
    visualize.execute(periods, unified, min_in_degrees, top, ind, repeats, replace, ordering_type, days, old)


if __name__ == '__main__':
    execute()

    print 'Done.'
