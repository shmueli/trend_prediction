import sys
sys.path.insert(0, '../')

import calc_returns
from helpers import constants


periods = constants.PERIODS_TRI_MONTHLY
days = 'end'
old = False


def execute():
    calc_returns.execute(periods, days, old)
    

if __name__ == '__main__':
    execute()

    print 'Done.'
