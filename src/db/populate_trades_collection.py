import pymongo


def execute():
    connection_string = "mongodb://localhost"
    
    connection = pymongo.MongoClient(connection_string)
    
    db = connection.trades

    
    db.trades.ensure_index('positionID')
    db.trades.ensure_index('CID')

    db.trades.ensure_index('openDate')
    db.trades.ensure_index('closeDate')

    db.trades.ensure_index('parentPositionID')
    db.trades.ensure_index('origParentPositionID')
    db.trades.ensure_index('mirrorID')
    db.trades.ensure_index('parentCID')
    
    db.trades.ensure_index('buyOrSell')    
    db.trades.ensure_index('buyCurAbbreviation')     
    db.trades.ensure_index('sellCurAbbreviation')
    

    db.trades.ensure_index([('buyCurAbbreviation', pymongo.ASCENDING), ('sellCurAbbreviation', pymongo.ASCENDING), ('openDate', pymongo.ASCENDING)])     


    '''
    #no need for indexes
    db.trades.ensure_index('amount')
    db.trades.ensure_index('leverage')
    db.trades.ensure_index('unitsDecimal')
    db.trades.ensure_index('openRate')    
    db.trades.ensure_index('closeRate')
    db.trades.ensure_index('spread')
    db.trades.ensure_index('nProfit')
    '''
    
    '''
    #ignored for now...
    'action' 
    'buyCurrencyTypeID' 
    'sellCurrencyTypeID' 
    'currencyBuy' 
    'currencySell' 
    'isBuy' 
    'instrument' 
    
    'units' 
    'profit' 
    
    'openRateFormated' 
    'closeRateFormated' 
    
    'limitRate' 
    'stopRate' 
    'gain' 
    'credit' 
    'gameName' 
    'version' 
    'isSocial' 
    '''


if __name__ == '__main__':
    execute()

    print 'Done.'