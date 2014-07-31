from datetime import datetime

input_folder = '/home/pway/Documents/tweet_jure/'
output_folder = '/home/shmueli/trend_prediction_data/tweeter/'

def loadFiles():
    records = []
    
    filenames = ['tweets2009-06.txt', 'tweets2009-07.txt', 'tweets2009-08.txt', 'tweets2009-09.txt', 'tweets2009-10.txt', 'tweets2009-11.txt', 'tweets2009-12.txt']
    filenames.sort()
    for filename in filenames:
        print 'Loading ' + filename
        loadFile(filename, records)
    
    records.sort()

    return records
            

def loadFile(filename, records):
    input_filename = input_folder + filename
    output_filename = output_folder + filename

    writer = open(output_filename, 'w')
    reader = open(input_filename, 'r')
    
    reader.readline()
    while True:
        line1 = reader.readline()
        if line1 == '':
            break;
        
        line1 = line1.strip()
        line2 = reader.readline().strip()
        line3 = reader.readline().strip()
        line4 = reader.readline().strip()
        
        #print line3
        
        if not line3[2:].startswith('RT'):
            continue
        
        dt = datetime.strptime(line1[2:], '%Y-%m-%d %H:%M:%S')
        
        follower = line2[2:].strip()
        if follower.find('/')>=0:
            follower = follower.split('/')[-1]
                
        followed = line3[5:].strip()
        if followed.find('@')>=0:
            followed = followed[1:]
        if followed.find(':')>=0:
            followed = followed.split(':')[0]
        if followed.find(' ')>=0:
            followed = followed.split(' ')[0]
        followed = followed.lower()
        
        line = str(dt) + ',' + follower + ',' + followed
        
        print line
        
        writer.write(line + '\n')
        
                
    reader.close()
    writer.close()
    

if __name__ == '__main__':
    loadFiles()

    print 'Done.'
