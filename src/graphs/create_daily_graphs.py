#commented so that it won't be executed by mistake...

# from datetime import datetime, timedelta
# 
# import helpers.constants as constants
# 
# 
# input_folder = constants.RAW_DATA_FOLDER_NAME
# output_folder = constants.GRAPHS_FOLDER_NAME
# 
# start = datetime.strptime('20110601000000', constants.GENERAL_DATE_FORMAT)
# end = datetime.strptime('20131201000000', constants.GENERAL_DATE_FORMAT)
# 
# shift = timedelta(seconds=int(150*60))
# 
# 
# files = {}
# max_files = 100
# 
# def execute():
#     initialize()
#     do_work()
#     finalize()
# 
#     
# def initialize():
#     global files
#     
#     time = start
#     while time < end:
#         output_filename = output_folder + time.strftime(constants.GENERAL_DATE_FORMAT)
#         
#         f = open(output_filename, 'w')
#         f.close()
#         
#         time = time + timedelta(days=1)
# 
# 
# def finalize():
#     print len(files)
#     for time, temp_file in files.iteritems():
#         temp_file.close()
# 
# 
# def do_work():
#     input_filename = input_folder + 'trades.csv'
#     input_file = open(input_filename, 'r')
# 
#     currDate = None
#     
#     header = input_file.readline().strip()
#     for line in input_file:
#         line = line.strip()
#         fields = line.split(',')
#         
#         openDate = datetime.strptime(fields[2], '%Y-%m-%dT%H:%M:%SZ') + shift
#         openDate = openDate.replace(second=0, minute=0, hour=0)
#         closeDate = datetime.strptime(fields[3], '%Y-%m-%dT%H:%M:%SZ') + shift
#         closeDate = closeDate.replace(second=0, minute=0, hour=0)
#     
#         if currDate==None or currDate<closeDate:
#             currDate = closeDate
#             print '###', currDate
#                 
#         time = openDate
#         while time<=closeDate:
#             if time>=start and time<=end:
#                 actual_write(time, line)
#             
#             time = time + timedelta(days=1)
#             
#     input_file.close()
# 
# def actual_write(time, line):
#     if time in files:
#         f = files[time]
#     else:
#         if len(files)>=max_files:
#             times = files.keys()
#             times.sort()
#             
#             old_time = times[0]
#             
#             files[old_time].close()
#             del files[old_time]
#         
#         output_filename = output_folder + time.strftime(constants.GENERAL_DATE_FORMAT)
#         f = open(output_filename, 'a')
#         files[time] = f
# 
#     f.write(line + '\n')
# 
# 
# if __name__ == '__main__':
#     execute()
# 
#     print 'Done.'
