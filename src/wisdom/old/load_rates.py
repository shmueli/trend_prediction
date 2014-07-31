import h5py

import helpers.constants as constants

from datetime import datetime, timedelta


def execute():
    input_filename = 'x:/workspace/trend_prediction_data/market_data/TrueFX data/AUD_JPY/pricesData4.mat'
    data = h5py.File(input_filename, 'r')
    
    a = data['M']['pricesData'][...]
    
    print len(a)
    
    print len(a[0])
    
    print a[0][0], a[1][0], a[2][0]
    
    dn = a[0][0]
    python_datetime = datetime.fromordinal(int(dn)) + timedelta(days=dn%1) - timedelta(days = 366)

    print python_datetime

if __name__ == '__main__':
    execute()