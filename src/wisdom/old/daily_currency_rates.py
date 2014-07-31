import datetime

import helpers.constants as constants


rates = None
instruments = None

def load():
    global rates
    global instruments

    input_folder = constants.MIRROR_FOLDER_NAME

    input_filename = input_folder + 'rates'

    
    
    rates = {}
    
    reader = open(input_filename, 'r')
    
    for line in reader:
        record = eval(line)
        
        dt = record[0]
        instrument = record[1]
        buy = record[2]
        
        if dt not in rates:
            rates[dt] = {}
        
        rates[dt][instrument] = buy
    
    reader.close()


    #complete weekends
    dates = rates.keys()
    for date in dates:    
        if date.weekday()==4: #Friday
            data = rates[date]
            
            date = date + datetime.timedelta(days=1)
            rates[date] = data
            
            date = date + datetime.timedelta(days=1)
            rates[date] = data

    instruments = rates[list(dates)[0]].keys()


def get_instruments():
    return instruments


def get_rate(instrument, time):
    if time not in rates:
        return None
    
    if instrument not in rates[time]:
        return None

    return rates[time][instrument]
