from db import load_graphs
from datetime import datetime, timedelta
import helpers.constants as constants


output_folder = constants.MIRROR_FOLDER_NAME


start = datetime.strptime('20110613000000', constants.GENERAL_DATE_FORMAT)
end = datetime.strptime('20131121000000', constants.GENERAL_DATE_FORMAT)

sensitivity = timedelta(seconds=int(constants.SENSITIVITY))


def execute():
    load_graphs.init_connection()
    
    time = start
    while time < end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT)

        output_filename = output_folder + time_str   

        g = load_graphs.load_time_network(time, data=False)
        
        f = open(output_filename, 'w')

        for e in g.edges():
            record = [e[0], e[1]]
            line = str(record)
            f.write(line + '\n')
                
        f.close()
        
        time = time + timedelta(days=1)


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
