import sys
sys.path.insert(0, '../')

import json

from helpers import constants
import load_rates


def execute():
    output_folder = constants.RATES_FOLDER_NAME
    
    rates = load_rates.load(24) #we assume that the last month is updated in terms of the available instruments...
    
    instruments = list(rates.keys())
    
    output_filename = output_folder + 'instruments'
    json.dump(instruments, open(output_filename, 'w'))
    

if __name__ == '__main__':
    execute()

    print 'Done.'
