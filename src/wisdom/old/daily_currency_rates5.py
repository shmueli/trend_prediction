from datetime import datetime, timedelta
import pymongo
import daily_currency_rates3


shift = timedelta(seconds=int(150*60))

db = None

def load():
    connection_string = "mongodb://localhost"
    
    connection = pymongo.MongoClient(connection_string)
  
    global db  
    db = connection.trades


def get_instruments():
    return [
#        "AAPL/USD",
#        "AMZN/USD",
        "AUD/JPY",
        "AUD/USD",
        "CAD/JPY",
        "CHF/JPY",
#        "DJ30/USD",
#        "EBAY/USD",
#        "EUR/AUD",
#        "EUR/CAD",
        "EUR/CHF",
        "EUR/GBP",
        "EUR/JPY",
        "EUR/USD",
#        "FB/USD",
        "FRA40/EUR",
        "GBP/JPY",
        "GBP/USD",
        "GER30/EUR",
        "GOLD/USD",
#        "GOOG/USD",
#        "MSFT/USD",
#        "NSDQ100/USD",
        "NZD/USD",
        "OIL/USD",
#        "SILVER/USD",
        "SPX500/USD",
        "UK100/GBP",
        "USD/CAD",
        "USD/CHF",
        "USD/JPY",
#        "YHOO/USD",
#        "ZNGA/USD"
    ]

    
def get_rate(curr1, curr2, time, accuracy=timedelta(minutes=1)):
    instrument = curr1 + '_' + curr2
    
    if time.weekday()==5:
        time = time + timedelta(days=2)
    elif time.weekday()==6:
        time = time + timedelta(days=1)
    #time = time-shift #todo
    
    rs = db.rates.find({'instrument': instrument, 'time': {'$gte': time}}).sort('time', 1).limit(1)

    t = next(rs)

    if t!=None:
        if t['time']-time > accuracy:
            #print instrument, t['OpenOccured']+shift-time, t
            return None
        
        return t['buy']

    return None
    