from datetime import datetime

from helpers import constants

def line_to_record(line):
    record = parse_line(line)

    record[0] = int(float(record[0]))
    record[1] = int(float(record[1]))
    record[2] = datetime.strptime(record[2], '%Y-%m-%dT%H:%M:%SZ')
    record[3] = datetime.strptime(record[3], '%Y-%m-%dT%H:%M:%SZ')
    record[4] = int(float(record[4]))
    record[5] = int(float(record[5]))
    record[6] = int(float(record[6]))
    record[7] = int(float(record[7]))
    record[8] = str(record[8])
    record[9] = str(record[9])
    record[10] = str(record[10])
    record[11] = float(record[11])
    record[12] = float(record[12])
                
    if record[13].find('e')>=0 and len(record[13])>2 and record[13][-2:]=='.0':
        record[13] = float(record[13][:-2]) 
    else:
        record[13] = float(record[13]) 
                
    record[14] = float(record[14])
    record[15] = float(record[15])
    record[16] = float(record[16])
    record[17] = float(record[17])
               
    follower = record[1]
    followed = record[7]
    
    if follower==0:
        print '$$$$$$$$$$ ERROR'
                
    #check with guy why this happens...
    if followed==0 or record[4]==0:
        followed = follower
        record[7] = record[1] #parentCID
        record[4] = record[0] #parentPositionID
        record[5] = record[0] #origParentPositionID

    t = {
        'positionID': record[0],
        'CID': record[1],
        'openDate': record[2],
        'closeDate': record[3],                
        'parentPositionID': record[4],
        'origParentPositionID': record[5],
        'mirrorID': record[6],
        'parentCID': record[7],
        'buyOrSell': record[8],
        'buyCurAbbreviation': record[9],
        'sellCurAbbreviation': record[10],
        'amount': record[11],
        'leverage': record[12],
        'unitsDecimal': record[13],
        'openRate': record[14],
        'closeRate': record[15],
        'spread': record[16],
        'nProfit': record[17],
    }

    return t


def parse_line(line):
    line = clean_line(line)
    record = line.strip().replace('"', '').split(',')
    
    return record


def clean_line(line):
    #handle the amount field which may contain a comma
    r = ''
    last = -1
    open_quote = False
    for i in range(len(line)):
        if line[i]=='"':
            open_quote = not open_quote
        if open_quote and line[i]==',':
            r = r + line[last+1:i]
            last = i
    if last<len(line)-1:
        r = r + line[last+1:]
                
    return r
