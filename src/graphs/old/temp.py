import sets
import sys
sys.path.insert(0, '../')

from datetime import datetime, timedelta

import helpers.constants as constants


input_folder = constants.RAW_DATA_FOLDER_NAME

def execute():
    do_work()

    
def do_work():
    a = sets.Set()
    b = []
    
    input_filename = input_folder + 'mirror.csv'
    input_file = open(input_filename, 'r')

    currDate = None
    
    header = input_file.readline().strip()
    for line in input_file:
        line = line.strip()
        fields = line.split(',')
        
        if fields[2] in a:
            print fields

        a.add(fields[2])
        b.append(fields[2])
            
    input_file.close()
    
    print len(a)
    print len(b)
    



if __name__ == '__main__':
    execute()

    print 'Done.'
