from datetime import datetime, timedelta


rates = None
instruments = None

def load():
    global rates
    global instruments

    input_folder = 'X:/workspace/trend_prediction_data/daily_currency_rates/'

    input_filename = input_folder + 'rates'

    
    
    rates = {}
    
    reader = open(input_filename, 'r')
    
    header = reader.readline()
    header_fields = header.strip().split(',')
    for line in reader:
        fields = line.strip().split(',')
        
        dt = datetime.strptime(fields[0], '%Y-%m-%d')
        
        if dt not in rates:
            rates[dt] = {}

        for i in range(1, len(header_fields)):
            instrument = header_fields[i]
            buy = float(fields[i])
            
            rates[dt][instrument] = buy
    
    reader.close()


    #complete weekends
    dates = rates.keys()
    for date in dates:    
        if date.weekday()==4: #Friday
            data = rates[date]
            
            date = date + timedelta(days=1)
            rates[date] = data
            
            date = date + timedelta(days=1)
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
