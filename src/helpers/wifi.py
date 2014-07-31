from datetime import datetime
import sets

_input_filename = 'X:/workspace/trend_prediction_data/wifi/observations.csv'
_output_folder = 'X:/workspace/trend_prediction_out/wifi/graphs/'

def processFile():
    nodes = sets.Set()
    co_occurence = {}
    
    i = 0
    reader = open(_input_filename, 'r')
    for line in reader:
        if i%10000==0:
            print i
        
        line = line.strip()
        fields = line.split(',')
        
        uid = fields[1][1:-1]
        building = fields[11][1:-1]
        building = building.strip()
        time = fields[19][1:-1]
        #time = time.replace('-', '/')
        time = time.replace('.txt', '')
        time = time.replace('-', '')
        time = time.replace(':', '')
        time = time.replace('_', '')
        time = time.replace(' ', '')
        
        if building=='':
            continue
        
        
        #print time
        
        dt = datetime.strptime(time, '%Y%m%d%H%M%S')
        dt = dt.replace(second=0)
        dt = dt.replace(minute = dt.minute/5*5)
        
        nodes.add(uid)
        
        day = dt.replace(second=0, minute=0, hour=0)
        if day not in co_occurence:
            co_occurence[day] = {}
        if (dt,building) not in co_occurence[day]:
            co_occurence[day][(dt,building)] = sets.Set()
        co_occurence[day][(dt,building)].add(uid)
        
        i = i+1
        #if i==100000:
        #    break

    print len(nodes)
    print len(co_occurence)
    
    reader.close()

    
    days = [day for day in co_occurence]
    days.sort()
    for day in days:
        datestr = datetime.strftime(day, '%Y%m%d%H%M%S')
        
        print datestr

        output_filename = _output_folder + datestr

        writer = open(output_filename, 'w')

        keys = [k for k in co_occurence[day].keys()]
        keys.sort()
        
        for (dt, building) in keys:
            nodes = co_occurence[day][(dt, building)]

            for v1 in nodes:
                for v2 in nodes:
                    if v1!=v2:            
                        #line = v1 + ',' + v2 + ',' + datetime.strftime(dt, '%Y%m%d%H%M%S') + ',' + building
                        line = v1 + ',' + v2
                        writer.write(line + '\n')
            
        writer.close()

    
if __name__ == '__main__':
    processFile()

    print 'Done.'
