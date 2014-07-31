import visualize_part1

min_in_degrees = [0, 1, 10]
repeats = 5

def execute():
    for min_in_degree in min_in_degrees:

        visualize_part1.predict_daily_currency_pair('random_' + str(min_in_degree) + '_1', norm_factor=repeats)
        visualize_part1.predict_daily_currency_pair('random_' + str(min_in_degree) + '_2', norm_factor=repeats)
        visualize_part1.predict_daily_currency_pair('random_' + str(min_in_degree) + '_3', norm_factor=repeats)
        visualize_part1.predict_daily_currency_pair('random_' + str(min_in_degree) + '_4', norm_factor=repeats)


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
