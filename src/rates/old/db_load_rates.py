from datetime import timedelta
import pymongo

shift = timedelta(seconds=int(150*60))
db = None

def load():
    connection_string = "mongodb://localhost"
    
    connection = pymongo.MongoClient(connection_string)
  
    global db  
    db = connection.trades


def get_instruments():
    return [
        "AAPL/USD",
        "AMZN/USD",
        "AUD/JPY",
        "AUD/USD",
        "CAD/JPY",
        "CHF/JPY",
        "DJ30/USD",
        "EBAY/USD",
        "EUR/AUD",
        "EUR/CAD",
        "EUR/CHF",
        "EUR/GBP",
        "EUR/JPY",
        "EUR/USD",
        "FB/USD",
        "FRA40/EUR",
        "GBP/JPY",
        "GBP/USD",
        "GER30/EUR",
        "GOLD/USD",
        "GOOG/USD",
        "MSFT/USD",
        "NSDQ100/USD",
        "NZD/USD",
        "OIL/USD",
        "SILVER/USD",
        "SPX500/USD",
        "UK100/GBP",
        "USD/CAD",
        "USD/CHF",
        "USD/JPY",
        "YHOO/USD",
        "ZNGA/USD"
    ]


def internal_get_rate(buyCurAbbreviation, sellCurAbbreviation, time):
    rs = db.trades.find({'buyCurAbbreviation': buyCurAbbreviation, 'sellCurAbbreviation': sellCurAbbreviation, 'openDate': {'$gte': time-shift}}).sort('openDate', 1).limit(1)

    return next(rs) #check


def get_rate(buyCurAbbreviation, sellCurAbbreviation, time, accuracy=timedelta(minutes=1)):
    global db
    if db==None:
        load()
        
    if time.weekday()==5:
        time = time + timedelta(days=2)
    elif time.weekday()==6:
        time = time + timedelta(days=1)

    t = internal_get_rate(buyCurAbbreviation, sellCurAbbreviation, time)
    
    '''
    if t==None or (t['OpenOccured']+shift-time)>timedelta(minutes=1):
        rate = internal_get_rate(instrument, time)

        if rate!=None:
            return rate
    '''

    if t!=None:
        if t['openDate']+shift-time > accuracy:
            #print instrument, t['OpenOccured']+shift-time, t
            return None
        
        return t['openRate']

    #print time, instrument
    return None
