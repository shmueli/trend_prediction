import sys
sys.path.insert(0, '../')

#import winning_strategy_part1
#import winning_strategy_part2
from wisdom import winning_strategy_ranked_daily
from wisdom import winning_strategy_random_daily


if __name__ == '__main__':
    #winning_strategy_part1.execute()
    #winning_strategy_part2.execute()
    winning_strategy_ranked_daily.execute()
    winning_strategy_random_daily.execute()

    print 'Done.'
