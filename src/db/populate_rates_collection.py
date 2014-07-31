from datetime import datetime, timedelta

import h5py
import pymongo


def execute():
    connection_string = "mongodb://localhost"
    
    connection = pymongo.MongoClient(connection_string)
    
    db = connection.trades

    db.rates.drop()

    db.rates.ensure_index([('instrument', pymongo.ASCENDING), ('time', pymongo.ASCENDING)])     


    instruments = [
        "AUD/JPY",
        "AUD/USD",
        "CAD/JPY",
        "CHF/JPY",
        #"EUR/AUD",
        #"EUR/CAD",
        "EUR/CHF",
        "EUR/GBP",
        "EUR/JPY",
        #"EUR/USD",
        "GBP/JPY",
        "GBP/USD",
        "NZD/USD",
        "USD/CAD",
        "USD/CHF",
        "USD/JPY"
    ]
    
    for instrument in instruments:

        print instrument
        
        instrument = instrument.replace('/', '_')
        
        input_filename = 'x:/workspace/trend_prediction_data/market_data/TrueFX data/' + instrument +'/pricesData_v73.mat'
        data = h5py.File(input_filename, 'r')
        
        data = data['pricesData'][...]
        
        documents = []
        
        size = len(data[0])
        for i in range(size):
            time = data[0][i]
            time = datetime.fromordinal(int(time)) + timedelta(days=time%1) - timedelta(days = 366)
            
            sell = data[1][i]
            buy = data[2][i]
    
            rate = {
                'instrument' : instrument,
                'time' : time,
                'sell' : sell,
                'buy' : buy
            }
        
            documents.append(rate)    
            #db.rates.insert(rate)
            
            if i%100000==0:
                print instrument, i, size
                db.rates.insert(documents)
                documents = []

        if len(documents)>0:
            db.rates.insert(documents)
            documents = []


if __name__ == '__main__':
    execute()

    print 'Done.'