from db import load_graphs
from datetime import datetime, timedelta
import helpers.constants as constants


output_folder = constants.GRAPHS_FOLDER_NAME

start = datetime.strptime('20110613000000', constants.GENERAL_DATE_FORMAT)
end = datetime.strptime('20131121000000', constants.GENERAL_DATE_FORMAT)

sensitivity = timedelta(seconds=int(constants.SENSITIVITY))


def execute():
    load_graphs.init_connection()
    
    time = start
    while (time+sensitivity)<=end:
        output_filename = output_folder + time.strftime(constants.GENERAL_DATE_FORMAT)
        
        g = load_graphs.load_time_network(time, data=True)
        
        f = open(output_filename, 'w')

        for e in g.edges(data=True):
            for t in e[2]['data']:
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
                f.write(line + '\n')
                
        f.close()
        
        time = time + sensitivity


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
