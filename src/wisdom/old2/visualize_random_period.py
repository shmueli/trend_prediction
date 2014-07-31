from wisdom import visualize_ranked_period

from helpers import constants


min_in_degrees = [0]
top = [str(t_int) for t_int in [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]]
ind = [str(i_int) for i_int in [0, 1, 2, -1]]
replace = ['true', 'false']
repeats = [str(j_int) for j_int in range(25)]
ordering_type = 'random'
returns_type = 'period'


def execute():
    for min_in_degree in min_in_degrees:
        for p in constants.PERIODS_TRI_MONTHLY:
            visualize_ranked_period.plot_all(top, ind, replace, repeats, ordering_type, returns_type, min_in_degree, p)


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
