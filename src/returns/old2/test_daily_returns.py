import sys
sys.path.insert(0, '../')

from datetime import datetime, timedelta

from graphs import csv_line_parser
from rates import load_rates as load_rates

from helpers import constants


def execute():
    input_filename = constants.RAW_DATA_FOLDER_NAME + 'trades.csv'
    input_file = open(input_filename, 'r')
 
    header = input_file.readline().strip()
    for line in input_file:
        
        t = csv_line_parser.line_to_record(line)

        p = 1
        if t['openDate']>=constants.PERIODS[p]['start'] and t['closeDate']<=constants.PERIODS[p]['end']:
            profit_in_usd, amount = calc_return_for_trade(t, t['openDate']+constants.SHIFT, t['closeDate']+constants.SHIFT, timedelta(days=1), 1)
        
        
    input_file.close()



def calc_return_for_trade(t, open_time, close_time, accuracy, period):    
    #Important insights:
    #1. I assume that the DollarAmount and AmountInUnitsDecimal fields are correct and that the Leverage field might be wrong...
    #2. NetProfit contains also the spread which may be a bit high for small profits
    #3. Guy database is not accurate enough - instead I use eToro's rate for other trades which occurred around the required time

    open_rate = load_rates.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], open_time, accuracy, period)
    close_rate = load_rates.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], close_time, accuracy, period)

    if open_rate==None or close_rate==None:
        #we didn't find accurate enough rates (i.e. rates around the required time)
        return None, None


    t_open_time = t['openDate'] + constants.SHIFT
    t_close_time = t['closeDate'] + constants.SHIFT
    t_open_rate = t['openRate']
    t_close_rate = t['closeRate']
    
    position_id = t['positionID']
    
    if open_time == t_open_time:
        if sig_diff(open_rate, t_open_rate, 1.1):
            print '###', 'open_rate', open_rate, t_open_rate, position_id
        open_rate = t_open_rate

    if close_time == t_close_time:
        if sig_diff(close_rate, t_close_rate, 1.1):
            print '###', 'close_rate', close_rate, t_close_rate, position_id
        close_rate = t_close_rate
        
    
    
    profit_delta = (close_rate-open_rate) * (1.0 if t['buyOrSell']=='Buy' else - 1.0)
    profit = t['unitsDecimal'] * profit_delta
    temp_rate = get_usd_rate(close_time, 'USD', t['sellCurAbbreviation'], t['buyCurAbbreviation'], period)
    if temp_rate==None:
        #we didn't find accurate enough rates (i.e. rates around the required time)
        if close_time.weekday()!=5 and close_time.weekday()!=6:
            print '***', close_time, 'USD', t['sellCurAbbreviation'], t['buyCurAbbreviation'], position_id
        return None, None        
    profit_in_usd = profit * temp_rate

    t_profit = t['nProfit'] - t['spread']
    if open_time == t_open_time and close_time == t_close_time:
        if sig_diff(profit_in_usd, t_profit, 2.0):
            print '$$$', 'profit', profit_in_usd, t_profit, str(t)
        profit_in_usd = t_profit


    '''    
    temp_rate = get_usd_rate(open_time, 'USD', t['buyCurAbbreviation'], t['sellCurAbbreviation'], period)
    if temp_rate==None:
        #we didn't find accurate enough rates (i.e. rates around the required time)
        if open_time.weekday()!=5 and open_time.weekday()!=6:
            print '###########################################################', open_time, 'USD', t['buyCurAbbreviation'], t['sellCurAbbreviation']
        return None, None        
    units_in_usd = t['unitsDecimal']*temp_rate
    
    t_units = t['amount']*t['leverage']
    '''

    amount = t['amount']

    return profit_in_usd, amount


def sig_diff(v1, v2, ratio):
    if is_zero(v1) and is_zero(v2):
        return False
    
    if is_zero(v1):
        return False

    if is_zero(v2):
        return False
    
    if v1<0.0 and v2>0.0:
        return True

    if v2<0.0 and v1>0.0:
        return True
    
    
    if ((v1/v2)>ratio) or ((v2/v1)>ratio):
        return True
    
    return False


def is_zero(v):
    zero = 0.000001

    if v>-zero and v<zero:
        return True
    else:
        return False

def get_usd_rate(close_time, target, source, mediator, period):
    if source==target:
        return 1.0
    
    buy = target
    sell = source
    instrument = buy + '/' + sell
    
    if instrument not in load_rates.get_instruments():
        buy = source
        sell = target    
        instrument = buy + '/' + sell

    if instrument not in load_rates.get_instruments():
        temp_rate1 = get_usd_rate(close_time, target, mediator, None, period)
        temp_rate2 = get_usd_rate(close_time, mediator, source, None, period)
        return temp_rate1*temp_rate2

    close_rate = load_rates.get_rate(buy, sell, close_time, timedelta(days=1), period)
    
    if close_rate==None:
        return None
    
        
    if sell==target:
        return close_rate
    
    if buy==target:
        return 1.0/close_rate


def tomorrow(time):
    tomorrow = datetime(time.year, time.month, time.day) + timedelta(days=1)
    return tomorrow


def period_length(start, end):
    diff = (end - start)
    period = diff.days + (1 if diff>timedelta(days=diff.days) else 0)

    return period


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
