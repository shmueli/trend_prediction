from datetime import datetime, timedelta

from db import load_graphs
import helpers.constants as constants


output_folder = constants.GRAPHS_FOLDER_NAME


output_file = None

def execute():
    initialize()
    do_work()
    finalize()

    
def initialize():
    global output_file
    
    output_filename = output_folder + 'graphs'
    
    output_file = open(output_filename, 'w')


def finalize():
    output_file.close()


def do_work():
    load_graphs.init_connection()

    db = load_graphs.get_db()
    trades = db.trades.find(timeout=False).sort('closeDate', 1)

    currDate = None
    
    for t in trades:
        record = [
            t['positionID'],
            t['CID'],
            t['openDate'],
            t['closeDate'],
            t['parentPositionID'],
            t['origParentPositionID'],
            t['mirrorID'],
            t['parentCID'],
            t['buyOrSell'],
            t['buyCurAbbreviation'],
            t['sellCurAbbreviation'],
            t['amount'],
            t['leverage'],
            t['unitsDecimal'],
            t['openRate'],
            t['closeRate'],
            t['spread'],
            t['nProfit'],
        ]

        line = str(record) 
    
        
        closeDate = t['closeDate']
        closeDate = closeDate.replace(second=0, minute=0, hour=0)

        if currDate==None or currDate<closeDate:
            currDate = closeDate
            print '###', currDate
        
        #print closeDate
        
        actual_write(line)
     

def actual_write(line):
    output_file.write(line + '\n')


if __name__ == '__main__':
    execute()

    print 'Done.'
    