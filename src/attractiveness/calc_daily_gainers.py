from datetime import datetime, timedelta
import json

from helpers import constants
from ranked_nodes import load_ranked_nodes
from returns import load_returns_1_new


history = 30

def execute():
    top_nodes = load_ranked_nodes.get_ranked_nodes()

    times = []
    pos = []
    neg = []
    
    
    for p in [2,3]:
        start = constants.PERIODS[p]['start']
        end = constants.PERIODS[p]['end']
    
        time = start
        while time<end:
            time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT) 

            cnt_pos = 0
            cnt_neg = 0
            for v in top_nodes:
                ROI = 0
                h = max(start, time - timedelta(days=history))
                while h<time:
                    r = load_returns_1_new.get_return(v, h, p)
                    roi = r[-1]
                    
                    if roi!=None:
                        ROI = ROI + roi
                        
                    h = h + timedelta(days=1)

                if ROI>0:
                    cnt_pos = cnt_pos + 1
                if ROI<0:
                    cnt_neg = cnt_neg + 1
                    
            times.append(time_str)
            pos.append(cnt_pos)
            neg.append(cnt_neg)
    
            print time, cnt_pos, cnt_neg
                
            time = time + timedelta(days=1)
    
    output_folder = constants.ATTRACTIVENESS_FOLDER_NAME
    json.dump(times, open(output_folder + 'times', 'w'))
    json.dump(pos, open(output_folder + 'pos', 'w'))
    json.dump(neg, open(output_folder + 'neg', 'w'))

    
#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
