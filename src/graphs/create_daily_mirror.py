import sys
sys.path.insert(0, '../')

from datetime import datetime, timedelta

import helpers.constants as constants


input_folder = constants.RAW_DATA_FOLDER_NAME
output_folder = constants.MIRROR_FOLDER_NAME

start = constants.PERIODS[1]['start']
end = constants.PERIODS[4]['end']

if constants.DATASET=='etoro':
    shift = timedelta(seconds=int(150*60))


files = {}
max_files = 100

def execute():
    initialize()
    do_work()
    finalize()

    
def initialize():
    global files
    
    time = start
    while time < end:
        output_filename = output_folder + time.strftime(constants.GENERAL_DATE_FORMAT)
        
        f = open(output_filename, 'w')
        f.close()
        
        time = time + timedelta(days=1)


def finalize():
    print len(files)
    for time, temp_file in files.iteritems():
        temp_file.close()


def do_work():
    input_filename = input_folder + 'mirror.csv'
    input_file = open(input_filename, 'r')

    currDate = None
    
    header = input_file.readline().strip()
    for line in input_file:
        line = line.strip()
        fields = line.split(',')
        
        if constants.DATASET=='etoro':
            openDate = datetime.strptime(fields[3], '%Y-%m-%dT%H:%M:%SZ') + shift
            openDate = openDate.replace(second=0, minute=0, hour=0)
            closeDate = datetime.strptime(fields[4], '%Y-%m-%dT%H:%M:%SZ') + shift
            closeDate = closeDate.replace(second=0, minute=0, hour=0)
    

        elif constants.DATASET=='call':
            openDate = datetime.strptime(fields[2], '%m/%d/%Y %H:%M')
            openDate = openDate.replace(second=0, minute=0, hour=0)
            closeDate = openDate + timedelta(days=14)
            
            
        elif constants.DATASET=='tweeter':
            openDate = datetime.strptime(fields[0], '%Y-%m-%d %H:%M:%S')
            openDate = openDate.replace(second=0, minute=0, hour=0)
            closeDate = openDate + timedelta(days=10)
            
            
    
        if currDate==None or currDate<closeDate:
            currDate = closeDate
            print '###', currDate

        time = openDate
        while time<=closeDate:
            if time>=start and time<=end:
                actual_write(time, line)
            
            time = time + timedelta(days=1)

            
    input_file.close()
    

def actual_write(time, line):
    if time in files:
        f = files[time]
    else:
        if len(files)>=max_files:
            times = files.keys()
            times.sort()
            
            old_time = times[0]
            
            files[old_time].close()
            del files[old_time]
        
        output_filename = output_folder + time.strftime(constants.GENERAL_DATE_FORMAT)
        f = open(output_filename, 'a')
        files[time] = f

    f.write(line + '\n')


if __name__ == '__main__':
    execute()

    print 'Done.'
