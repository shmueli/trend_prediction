import pymongo


def execute():
    connection_string = "mongodb://localhost"
    
    connection = pymongo.MongoClient(connection_string)
    
    db = connection.trades

    db.sample.drop()
    
    '''
    for trade in db.trades.find().limit(10):
        db.sample.insert(trade)
    '''

    size = db.trades.count()
    
    cnt = 0
    bad = 0
    for trade in db.trades.find(timeout=False):
        positionID = trade['positionID']
        parentPositionID = trade['parentPositionID']
        if parentPositionID==0:
            parentCID = 0
        else:
            parentTrade = db.trades.find_one({'positionID' : parentPositionID})
            if parentTrade != None:
                parentCID = parentTrade['CID']        
            else:
                print '#########', positionID, parentPositionID, trade
                parentCID = -1
                bad = bad + 1
        
        trade['parentCID'] = parentCID
        db.trades.save(trade)
        
        if cnt%1000==0:
            print cnt, size
        
        cnt = cnt+1
    
    print 'bad', bad, size


if __name__ == '__main__':
    execute()

    print 'Done.'