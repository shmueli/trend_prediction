import sys
sys.path.insert(0, '../')

import json
from datetime import datetime

from graphs import csv_line_parser

from helpers import constants


def execute():
    input_filename = constants.RAW_DATA_FOLDER_NAME + 'trades.csv'
    output_folder = constants.RATES_FOLDER_NAME

    rates = {}

    input_file = open(input_filename, 'r')
    
    cnt = 0
       
    input_file.readline()
    for line in input_file:
        cnt = cnt + 1
        
        fields = csv_line_parser.parse_line(line)
        
        openDateStr = fields[2].replace('-', '').replace(':', '').replace('T', '').replace('Z', '')
        closeDateStr = fields[3].replace('-', '').replace(':', '').replace('T', '').replace('Z', '')        
        
        if cnt%10000==0:
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@', closeDateStr
        #if cnt==1000000:
        #    break
        
        openRate = float(fields[14])
        closeRate = float(fields[15])
        if openRate/closeRate>float(2) or closeRate/openRate>float(2):
            print '###', openRate, closeRate
            continue 
        
        buyCurAbbreviation = fields[9].replace('"', '')
        sellCurAbbreviation = fields[10].replace('"', '')
        currency = buyCurAbbreviation + '/' + sellCurAbbreviation            

        openDate = datetime.strptime(openDateStr, constants.GENERAL_DATE_FORMAT)
        closeDate = datetime.strptime(closeDateStr, constants.GENERAL_DATE_FORMAT)
        
        p = constants.get_period(constants.PERIODS_MONTHLY, openDate)
        if p!=None:
            if p not in rates:
                rates[p] = {}
            if currency not in rates[p]:
                rates[p][currency] = {}
            if openDateStr not in rates[p][currency]:
                rates[p][currency][openDateStr] = openRate

        p = constants.get_period(constants.PERIODS_MONTHLY, closeDate)
        if p!=None:
            if p not in rates:
                rates[p] = {}
            if currency not in rates[p]:
                rates[p][currency] = {}
            if closeDateStr not in rates[p][currency]:
                rates[p][currency][closeDateStr] = closeRate
            
    input_file.close()
    
    for p in rates:
        for currency in rates[p]:
            ordered_times = []
            for date in rates[p][currency]:
                ordered_times.append([date, rates[p][currency][date]])
            rates[p][currency] = sorted(ordered_times)

    for p in rates:
        output_filename = output_folder + 'rates_' + str(p)
        json.dump(rates[p], open(output_filename, 'w'))
    

if __name__ == '__main__':
    execute()

    print 'Done.'
