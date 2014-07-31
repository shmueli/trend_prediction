from datetime import datetime, timedelta
import os
import pymongo

import helpers.constants as constants


output_folder = constants.GRAPHS_FOLDER_NAME

start = datetime.strptime(constants.START_DATE, constants.GENERAL_DATE_FORMAT)
end = datetime.strptime(constants.END_DATE, constants.GENERAL_DATE_FORMAT)

sensitivity = timedelta(seconds=int(constants.SENSITIVITY))

period = eval(constants.PERIOD)

if constants.DATASET == 'etoro':
    shift = timedelta(seconds=int(150*60))

db = None


def execute():
    initialize()
    loadFiles()
    finalize()

    
def initialize():
    connection_string = "mongodb://localhost"
    
    connection = pymongo.MongoClient(connection_string)
    
    global db
    db = connection.etoro

    '''
    if 'trades' in db.collection_names():
        db.trades.drop()
        
    db.trades.ensure_index('SocialType')
    db.trades.ensure_index('PositionID')
    db.trades.ensure_index('ParentPositionID')
    db.trades.ensure_index('GCID')
    db.trades.ensure_index('ParentGCID')
    
    db.trades.ensure_index('OpenOccured')
    db.trades.ensure_index('CloseOccured')
    
    db.trades.ensure_index('NetProfit')
    db.trades.ensure_index('Instrument')
    db.trades.ensure_index('DealSide')
    db.trades.ensure_index('DollarsAmount')
    db.trades.ensure_index('AmountInUnitsDecimal')
    db.trades.ensure_index('InitForexRate')
    db.trades.ensure_index('Leverage')
    
    db.trades.ensure_index('MirrorID')
    '''
        
    return


def finalize():
    #do nothing
    return


def loadFiles():
    filenames = os.listdir(constants.RAW_DATA_FOLDER_NAME)
    filenames.sort()
    for filename in filenames:
        print 'Loading ' + filename
        #if filename.find('close')>=0:
        #    handleCloseFile(filename)
        if filename.find('open')>=0:
            handleOpenFile(filename)
        

def handleCloseFile(filename):
    input_filename = constants.RAW_DATA_FOLDER_NAME + filename

    reader = open(input_filename, mode='r')
    line = reader.readline()
    print line

    for line in reader:
        line = line.strip()

        fields = line.split('\t')
        
        SocialType = fields[5]
        PositionID = int(fields[0])
        GCID = int(fields[2])
        if SocialType=='Non-social':
            ParentPositionId = PositionID
            ParentGCID = GCID
        else:
            ParentPositionId = int(fields[14])
            ParentGCID = int(fields[17])

        OpenOccured = datetime.strptime(fields[4], constants.RAW_DATE_FORMAT)
        CloseOccured = datetime.strptime(fields[7], constants.RAW_DATE_FORMAT)
        
        NetProfit = float(fields[6])
        Instrument = fields[8]
        DealSide = fields[9]
        DollarsAmount = float(fields[10])
        AmountInUnitsDecimal = float(fields[11])
        InitForexRate = float(fields[12])
        Leverage = float(fields[13])
        
        MirrorID = int(fields[15])
        
        trade = {
            'SocialType': SocialType,
            'PositionID': PositionID,
            'ParentPositionID': ParentPositionId,
            'GCID': GCID,
            'ParentGCID': ParentGCID,

            'OpenOccured': OpenOccured,
            'CloseOccured': CloseOccured,                

            'NetProfit': NetProfit,
            'Instrument': Instrument,
            'DealSide': DealSide,
            'DollarsAmount': DollarsAmount,
            'AmountInUnitsDecimal': AmountInUnitsDecimal,
            'InitForexRate': InitForexRate,
            'Leverage': Leverage,

            'MirrorID': MirrorID,
        }
        

        print CloseOccured, PositionID
        if CloseOccured<datetime.strptime('20130601000000', constants.GENERAL_DATE_FORMAT):
            continue
        existing = False
        rs = db.trades.find({'PositionID': PositionID}).limit(1)
        for temp in rs:
            existing = True
        if existing:
            continue
            

        db.trades.insert(trade)    


def handleOpenFile(filename):
    input_filename = constants.RAW_DATA_FOLDER_NAME + filename

    reader = open(input_filename, mode='r')
    line = reader.readline()
    print line

    for line in reader:
        line = line.strip()

        fields = line.split('\t')
        
        SocialType = fields[5]
        PositionID = int(fields[0])
        GCID = int(fields[2])
        if SocialType=='Non-social':
            ParentPositionId = PositionID
            ParentGCID = GCID
        else:
            ParentPositionId = int(fields[13])
            ParentGCID = int(fields[16])

        OpenOccured = datetime.strptime(fields[4], constants.RAW_DATE_FORMAT)
        CloseOccured = None
        
        NetProfit = float(fields[6])
        Instrument = fields[7]
        DealSide = fields[8]
        DollarsAmount = float(fields[9])
        AmountInUnitsDecimal = float(fields[10])
        InitForexRate = float(fields[11])
        Leverage = float(fields[12])
        
        MirrorID = int(fields[14])
        
        trade = {
            'SocialType': SocialType,
            'PositionID': PositionID,
            'ParentPositionID': ParentPositionId,
            'GCID': GCID,
            'ParentGCID': ParentGCID,

            'OpenOccured': OpenOccured,
            'CloseOccured': CloseOccured,                

            'NetProfit': NetProfit,
            'Instrument': Instrument,
            'DealSide': DealSide,
            'DollarsAmount': DollarsAmount,
            'AmountInUnitsDecimal': AmountInUnitsDecimal,
            'InitForexRate': InitForexRate,
            'Leverage': Leverage,

            'MirrorID': MirrorID,
        }
        

        print OpenOccured, PositionID
        
        '''
        if CloseOccured<datetime.strptime('20130601000000', constants.GENERAL_DATE_FORMAT):
            continue
        existing = False
        rs = db.trades.find({'PositionID': PositionID}).limit(1)
        for temp in rs:
            existing = True
        if existing:
            continue
        '''    

        db.trades.insert(trade)    


if __name__ == '__main__':
    execute()

    print 'Done.'