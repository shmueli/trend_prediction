from datetime import datetime, timedelta


DATASET = 'etoro'

BASE_FOLDER = 'x:/workspace/'

RAW_DATA_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_data/eToro/'
GRAPHS_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/graphs/'
MIRROR_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/mirror/'
RANKED_NODES_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/ranked_nodes/'
RATES_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/rates/'
RETURNS_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/returns/'
POPULARITY_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/popularity/'
ATTRACTIVENESS_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/attractiveness/'
DYNAMICS_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/dynamics/'
WISDOM_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/wisdom/'
STATS_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/stats/'

CHARTS_FOLDER_NAME = BASE_FOLDER + 'trend_prediction_out/charts/'


PERIODS_MONTHLY = {
    #0: {'start': datetime.strptime('20110601000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20110701000000', '%Y%m%d%H%M%S')},
    
    1: {'start': datetime.strptime('20110701000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20110801000000', '%Y%m%d%H%M%S')},
    2: {'start': datetime.strptime('20110801000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20110901000000', '%Y%m%d%H%M%S')},
    3: {'start': datetime.strptime('20110901000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20111001000000', '%Y%m%d%H%M%S')},
    4: {'start': datetime.strptime('20111001000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20111101000000', '%Y%m%d%H%M%S')},
    5: {'start': datetime.strptime('20111101000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20111201000000', '%Y%m%d%H%M%S')},
    6: {'start': datetime.strptime('20111201000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120101000000', '%Y%m%d%H%M%S')},
    7: {'start': datetime.strptime('20120101000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120201000000', '%Y%m%d%H%M%S')},
    8: {'start': datetime.strptime('20120201000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120301000000', '%Y%m%d%H%M%S')},
    9: {'start': datetime.strptime('20120301000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120401000000', '%Y%m%d%H%M%S')},
    10: {'start': datetime.strptime('20120401000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120501000000', '%Y%m%d%H%M%S')},
    11: {'start': datetime.strptime('20120501000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120601000000', '%Y%m%d%H%M%S')},
    12: {'start': datetime.strptime('20120601000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120701000000', '%Y%m%d%H%M%S')},
    13: {'start': datetime.strptime('20120701000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120801000000', '%Y%m%d%H%M%S')},
    14: {'start': datetime.strptime('20120801000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120901000000', '%Y%m%d%H%M%S')},
    15: {'start': datetime.strptime('20120901000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20121001000000', '%Y%m%d%H%M%S')},
    16: {'start': datetime.strptime('20121001000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20121101000000', '%Y%m%d%H%M%S')},
    17: {'start': datetime.strptime('20121101000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20121201000000', '%Y%m%d%H%M%S')},
    18: {'start': datetime.strptime('20121201000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130101000000', '%Y%m%d%H%M%S')},
    19: {'start': datetime.strptime('20130101000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130201000000', '%Y%m%d%H%M%S')},
    20: {'start': datetime.strptime('20130201000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130301000000', '%Y%m%d%H%M%S')},
    21: {'start': datetime.strptime('20130301000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130401000000', '%Y%m%d%H%M%S')},
    22: {'start': datetime.strptime('20130401000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130501000000', '%Y%m%d%H%M%S')},
    23: {'start': datetime.strptime('20130501000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130601000000', '%Y%m%d%H%M%S')},
    24: {'start': datetime.strptime('20130601000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130701000000', '%Y%m%d%H%M%S')},

    25: {'start': datetime.strptime('20130701000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130801000000', '%Y%m%d%H%M%S')},
    26: {'start': datetime.strptime('20130801000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130901000000', '%Y%m%d%H%M%S')},
    27: {'start': datetime.strptime('20130901000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20131001000000', '%Y%m%d%H%M%S')},
}

SHIFT = timedelta(seconds=int(150*60))


DELIMITER = '\t'

RAW_DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
GENERAL_DATE_FORMAT = '%Y%m%d%H%M%S'


def get_period(periods, time):
    for p in periods:
        if time>=periods[p]['start'] and time<periods[p]['end']:
            return p
    return None

'''
def get_period_monthly(time):
    for p in PERIODS_MONTHLY:
        if time>=PERIODS_MONTHLY[p]['start'] and time<PERIODS_MONTHLY[p]['end']:
            return p
    return None

def get_period_tri_monthly(time):
    for p in PERIODS_TRI_MONTHLY:
        if time>=PERIODS_TRI_MONTHLY[p]['start'] and time<PERIODS_TRI_MONTHLY[p]['end']:
            return p
    return None
'''