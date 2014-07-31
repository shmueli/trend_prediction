from datetime import datetime, timedelta
import helpers.constants as constants
import os
import math

output_folder = constants.GRAPHS_FOLDER_NAME

start = datetime.strptime(constants.START_DATE, constants.GENERAL_DATE_FORMAT)
end = datetime.strptime(constants.END_DATE, constants.GENERAL_DATE_FORMAT)

sensitivity = timedelta(seconds=int(constants.SENSITIVITY))

period = eval(constants.PERIOD)

if constants.DATASET == 'etoro':
    shift = timedelta(seconds=int(150*60))


files = {}
max_files = 100

def execute():
    initialize()
    loadFiles()
    finalize()

    
def initialize():
    global files
    
    time = start
    while (time+sensitivity)<=end:
        output_filename = output_folder + time.strftime(constants.GENERAL_DATE_FORMAT)
        
        f = open(output_filename, 'w')
        f.close()
        
        time = time + sensitivity


def finalize():
    print len(files)
    for time, temp_file in files.iteritems():
        temp_file.close()


def loadFiles():
    filenames = os.listdir(constants.RAW_DATA_FOLDER_NAME)
    filenames.sort()
    for filename in filenames:
        print 'Loading ' + filename
        loadFile(filename)
        

def loadFile(filename):
    input_filename = constants.RAW_DATA_FOLDER_NAME + filename

    reader = open(input_filename, mode='r')
    line = reader.readline()
    print line

    for line in reader:
        line = line.strip()
        
        if constants.DATASET == 'etoro':
            fields = line.split('\t')
            
            SocialType = fields[5]
            PositionId = int(fields[0])
            GCID = int(fields[2])
            if SocialType=='Non-social':
                ParentPositionId = PositionId
                ParentGCID = GCID
            else:
                ParentPositionId = int(fields[14])
                ParentGCID = int(fields[17])

            OpenOccured = datetime.strptime(fields[4], constants.RAW_DATE_FORMAT) + shift
            CloseOccured = datetime.strptime(fields[7], constants.RAW_DATE_FORMAT) + shift
            
            NetProfit = float(fields[6])
            Instrument = fields[8]
            DealSide = fields[9]
            DollarsAmount = float(fields[10])
            AmountInUnitsDecimal = float(fields[11])
            InitForexRate = float(fields[12])
            Leverage = float(fields[13])
            
            MirrorID = int(fields[15])
            
            record = [
                SocialType,
                PositionId,
                ParentPositionId,
                GCID,
                ParentGCID,
                OpenOccured,
                CloseOccured,
                NetProfit,
                Instrument,
                DealSide,
                DollarsAmount,
                AmountInUnitsDecimal,
                InitForexRate,
                Leverage,
                MirrorID,
            ]
        
            append_record(record)
        
        
        elif constants.DATASET == 'call' or constants.DATASET == 'sms' or constants.DATASET == 'bt':
            fields = line.split(',')

            follower = fields[0]
            followed = fields[1]
            openDT = datetime.strptime(fields[2], '%m/%d/%Y %H:%M')

            if follower[:2]!='FA' and follower[:2]!='SP':
                continue
            if followed[:2]!='FA' and followed[:2]!='SP':
                continue
             
            if constants.DATASET=='call' or constants.DATASET=='sms':
                if fields[3] == 'INCOMING':
                    temp = followed
                    followed = follower
                    follower = temp
                    
            record = [follower, followed, openDT]
            append_record(record) 


def append_record(record):
    line = str(record) 

    if constants.DATASET == 'etoro':
        openDT = record[5]
        closeDT = record[6]
        
    elif constants.DATASET == 'call' or constants.DATASET == 'sms' or constants.DATASET == 'bt':
        openDT = record[2]
        closeDT = None
        
    
    diff1 = openDT - start
    n1 = int( math.floor( diff1.total_seconds() / sensitivity.total_seconds() ) )

    if closeDT==None:
        n2 = n1
    else:
        diff2 = closeDT - start
        n2 = int(diff2.total_seconds() / sensitivity.total_seconds())

        if openDT.weekday()==5:
            n1 = n1-1
        if openDT.weekday()==6:
            n1 = n1+1
        if closeDT.weekday()==5:
            n2 = n2-1
        if closeDT.weekday()==6:
            n2 = n2+1

    for n in range(n1, n2+1):
        time = start + (n * sensitivity)
        
        if time<start or time>end:
            continue

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
