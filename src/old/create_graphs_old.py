from datetime import datetime, timedelta
import helpers.constants as constants
import os
import math

output_folder = constants.GRAPHS_FOLDER_NAME

start = datetime.strptime(constants.START_DATE, constants.GENERAL_DATE_FORMAT)
end = datetime.strptime(constants.END_DATE, constants.GENERAL_DATE_FORMAT)

sensitivity = timedelta(seconds=int(constants.SENSITIVITY))
period = timedelta(seconds=int(constants.PERIOD))

files = {}
max_files = 3

def execute():
    initialize()
    loadFiles()
    finalize()

    
def initialize():
    global files
    
    time = start+period
    while time<=end:
        output_filename = output_folder + time.strftime(constants.GENERAL_DATE_FORMAT)
        
        f = open(output_filename, 'w')
        f.close()
        
        time = time + sensitivity


def finalize():
    for time, temp_file in files.iter_items():
        temp_file.close()


def loadFiles():
    filenames = os.listdir(constants.RAW_DATA_FOLDER_NAME)
    filenames.sort()
    for filename in filenames:
        print 'Loading ' + filename
        loadFile(filename)
        

def loadFile(filename):
    input_filename = constants.RAW_DATA_FOLDER_NAME + filename

    #reader = codecs.open(input_filename, mode='r', encoding='utf-8-sig')
    reader = open(input_filename, mode='r')
    #line = reader.readline()
    for line in reader:
        #line = line.decode("utf-8-sig")
        #line = line.encode("utf-8")
        line = line.strip()
        fields = line.split(constants.DELIMITER)        


        if constants.DATASET=='etoro':
            fields = line.split('\t')
            
            if fields[0]=='RealCID':
                continue
                
            if len(fields)<17:
                continue
            if fields[7]!='EUR/USD':
                continue
            if fields[4]=='Non-social':
                continue
        
        filter_index = int(constants.FILTER_INDEX)
        if filter_index>=0:
            filter_value = constants.FILTER_VALUE
            if fields[filter_index]!=filter_value:
                continue

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

        if constants.DATASET!='etoro':
            if (follower[:2]!='SP' and follower[:2]!='FA') or (followed[:2]!='SP' and followed[:2]!='FA'):
                continue
    
            if len(fields)>3:
                if fields[3]=='OUTGOING':
                    append_record(follower, followed, dt)
                else:
                    append_record(followed, follower, dt)
            else:
                append_record(follower, followed, dt)
                append_record(followed, follower, dt)
                
            continue

        append_record(follower, followed, dt) 


def append_record(follower, followed, dt):
    #line = follower + '\t' + followed + '\t' + dt.strftime(constants.GENERAL_DATE_FORMAT)
    line = follower + '\t' + followed

    if dt>=end or dt<start:
        return;
    
    diff = dt - start
    n = math.floor(diff.total_seconds() / sensitivity.total_seconds())
    periodStart = start + timedelta(seconds = (n * sensitivity.total_seconds()))
    periodEnd = periodStart + period 
    
    times = []
    while periodEnd>=(start+period) and periodEnd<=end and periodEnd>dt:
        times.append(periodEnd)
        
        periodStart = periodStart - sensitivity
        periodEnd = periodEnd - sensitivity
        
    for time in times:
        actual_write(time, line)
        


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
