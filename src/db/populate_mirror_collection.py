import pymongo
from bson.code import Code

rates = None
instruments = None

def execute():
    connection_string = "mongodb://localhost"
    
    connection = pymongo.MongoClient(connection_string)
    
    db = connection.trades
    
    mapS = '''
        function() {
            emit(
                this.mirrorID,
                {
                    mirrorID: this.mirrorID,
                    CID: this.CID,
                    parentCID: this.parentCID}
                    openDate: this.openDate,
                    closeDate: this.closeDate,
                );
        }
    '''
    
    reduceS = '''
        function(key, values) {
            var minDT=values[0][\'openDate\'];
            for (var i=1; i<values.length; i++) {
                temp = values[i][\'openDate\'];
                if (temp==null || minDT==null)
                    minDT=null;
                else if (temp<minDT)
                    minDT = temp;
            }
            
            var maxDT=values[0][\'closeDate\'];
            for (var i=1; i<values.length; i++) {
                temp = values[i][\'closeDate\'];
                if (temp==null || maxDT==null)
                    maxDT=null;
                else if (temp>maxDT)
                    maxDT = temp;
            }
            
            var pCID=values[0][\'parentCID\'];
            for (var i=1; i<values.length; i++) {
                temp = values[i][\'parentCID\'];
                if (pCID==0 || pCID==-1)
                    pCID=temp;
                }
                return {
                    mirrorID: key,
                    CID: values[0][\'CID\'],
                    parentCID: pCID,
                    openDate: minDT,
                    closeDate: maxDT
                };
        }
    '''
    
    db.trades.map_reduce(Code(mapS), Code(reduceS), 'temp_mirror')
    
    db.mirror.drop()
    
    db.mirror.ensure_index('CID')
    db.mirror.ensure_index('parentCID')    
    db.mirror.ensure_index('openDate')
    db.mirror.ensure_index('closeDate')
    db.mirror.ensure_index('mirrorID')

    for e in db.temp_mirror.find():
        db.mirror.insert(e['value'])
    
#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
