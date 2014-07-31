from db import load_graphs
import helpers.constants as constants


output_folder = constants.MIRROR_FOLDER_NAME


output_file = None

def execute():
    initialize()
    do_work()
    finalize()

    
def initialize():
    global output_file
    
    output_filename = output_folder + 'mirror'
    
    output_file = open(output_filename, 'w')


def finalize():
    output_file.close()


def do_work():
    load_graphs.init_connection()

    db = load_graphs.get_db()
    trades = db.mirror.find(timeout=False).sort('closeDate', 1)

    currDate = None
    
    for t in trades:
        record = [
            #t['mirrorID'],
            t['CID'],
            t['parentCID'],
            t['openDate'],
            t['closeDate'],
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
