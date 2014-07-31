import helpers.constants as constants

from datetime import datetime
import os

def loadFiles():
    records = []
    
    filenames = os.listdir(constants.RAW_DATA_FOLDER_NAME)
    filenames.sort()
    for filename in filenames:
        print 'Loading ' + filename
        loadFile(filename, records)
    
    records.sort()

    return records
            

def loadFile(filename, records):
    input_filename = constants.RAW_DATA_FOLDER_NAME + filename

    reader = open(input_filename, 'r')
    for line in reader:
        line = line.strip()
        fields = line.split('\t')        

        if fields[7]!='EUR/USD':
            continue
        if len(fields)<17:
            continue
        if fields[4]=='Non-social':
            continue

        '''
        filter_index = int(constants.FILTER_INDEX)
        if filter_index>=0:
            filter_value = constants.FILTER_VALUE
            if fields[filter_index]!=filter_value:
                continue
        '''

        from_index = int(constants.FROM_INDEX)
        to_index = int(constants.TO_INDEX)
        time_index = int(constants.TIME_INDEX)

        follower = fields[from_index]
        followed = fields[to_index]
        time = fields[time_index]

        dt = datetime.strptime(time, constants.RAW_DATE_FORMAT)
        
        start = datetime.strptime(constants.START_DATE, constants.GENERAL_DATE_FORMAT)
        end = datetime.strptime(constants.END_DATE, constants.GENERAL_DATE_FORMAT)
        
        if dt<start or dt>end:
            continue

        '''
        if (follower[:2]!='SP' and follower[:2]!='FA') or (followed[:2]!='SP' and followed[:2]!='FA'):
            continue
        
        if len(fields)>3 and fields[3]!='OUTGOING':
            continue
        '''
        
        record = [dt, follower, followed]

        records.append(record)
