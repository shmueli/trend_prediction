import pymongo

import helpers.constants as constants


def execute():
    connection_string = "mongodb://localhost"
    
    connection = pymongo.MongoClient(connection_string)
    
    db = connection.rates
    
 
    
    output_folder = constants.MIRROR_FOLDER_NAME

    output_filename = output_folder + 'rates'

    f = open(output_filename, 'w')

    temp = db.rates.find()
    for t in temp:
        dt = t['date']

        if dt.hour==0 and dt.minute==0:
            record = [t['date'], t['instrument'], t['buy'], t['sell']]
            line = str(record)
            
            print line
            f.write(line + '\n')
            
    f.close()


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
