import sys
sys.path.insert(0, '../')

import json
from datetime import datetime

_popularity = None
_period = None


def load(period):
    global _period, _popularity

    if _period==period:
        return

    input_filename = 'X:/workspace/trend_prediction_out/etoro/daily_period/popularity/daily_popularity'
    
    _popularity = json.load(open(input_filename, 'r'))


load(1)
print len(_popularity)
for v in _popularity:
    date_str = '20110701000000'
    if date_str in _popularity[v]:
        print _popularity[v][date_str]