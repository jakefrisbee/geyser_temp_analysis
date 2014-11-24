# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 17:17:08 2014

@author: Jake
"""
import peak_detection_class as pdc
import gtapi_private as gtapip
import time

run_these = { 'Artemisia' }

params = {
'Aurum': {'geyserID': 10, 'loggerID': 4, 'filter_width': 60, 'snr': 100, 'jump_or_max': 'max', 'jump_window': 60},
'Beehive': {'geyserID': 1, 'loggerID': 5, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'max', 'jump_window': 300},
'Castle': {'geyserID': 5, 'loggerID': 6, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'max', 'jump_window': 60},
'Daisy': {'geyserID': 4, 'loggerID': 7, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'jump', 'jump_window': 120},
'Grand': {'geyserID': 13, 'loggerID': 10, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'jump', 'jump_window': 240},
'Great Fountain': {'geyserID': 16, 'loggerID': 11, 'filter_width': 60, 'snr': 30, 'jump_or_max': 'first_jump', 'jump_window': 120},
'Lion': {'geyserID': 14, 'loggerID': 13, 'filter_width': 60, 'snr': 25, 'jump_or_max': 'max', 'jump_window': 10},
'Little Squirt': {'geyserID': 36, 'loggerID': 14, 'filter_width': 60, 'snr': 10, 'jump_or_max': 'max', 'jump_window': 10},
'Oblong': {'geyserID': 23, 'loggerID': 15, 'filter_width': 60, 'snr': 15, 'jump_or_max': 'max', 'jump_window': 120},
'Old Faithful': {'geyserID': 2, 'loggerID': 16, 'filter_width': 90, 'snr': 20, 'jump_or_max': 'max', 'jump_window': 30},
'Plume': {'geyserID': 3, 'loggerID': 17, 'filter_width': 60, 'snr': 100, 'jump_or_max': 'max', 'jump_window': 10},
'Turban': {'geyserID': 28, 'loggerID': 20, 'filter_width': 60, 'snr': 100, 'jump_or_max': 'max', 'jump_window': 10},
#duration
'Artemisia': {'geyserID': 19, 'loggerID': 3, 'filter_width': 60, 'snr': 100, 'jump_or_max': 'first_jump', 'jump_window': 300, 
              'duration_by_big_drop':
                          {
                          'look_ahead': 50,
                          'decrease_in_row': 10,
                          'points_from_big_drop': 0
                          }
            },
'Fountain': {'geyserID': 15, 'loggerID': 9, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'first_jump', 'jump_window': 120, 
             'duration': { 
                          'duration_end_point': 2, 
                          'decrease_length': 14,   #of points to look for decreasing temperatures
                          'decrease_count_threshold': 12,  # of points that must be decreasing
                          'first_x_decreasing': 10,
                          'look_ahead': 50, # points into the future to look for temperature dropoff
                          }
            },
'Grotto': {'geyserID': 21, 'loggerID': 12, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'first_jump', 'jump_window': 120, 
           'duration': { 'duration_end_point': 2, 
                        'decrease_length': 20, # # of points to look for decreasing temperatures
                        'decrease_count_threshold': 20, # # of points that must be decreasing
                        'look_ahead': 2000, # points into the future to look for temperature dropoff
                        }
           },
'Spouter': {'geyserID': 50, 'loggerID': 19, 'filter_width': 60, 'snr': 20, 'jump_or_max': 'first_jump', 'jump_window': 30, 
            'duration': { 'duration_end_point': 3, 
                        'decrease_length': 10, # # of points to look for decreasing temperatures
                        'decrease_count_threshold': 10, #  of points that must be decreasing
                        'first_x_decreasing': 8,
                        'look_ahead': 200 # points into the future to look for temperature dropoff
                        }
            },
#YVO
'Echinus': {'geyserID': 81, 'loggerID': 23, 'filter_width': 30, 'snr': 50, 'jump_or_max': 'max', 'jump_window': 300, 'duration': 0},
'Steamboat': {'geyserID': 163, 'loggerID': 21, 'filter_width': 30, 'snr': 50, 'jump_or_max': 'max', 'jump_window': 300, 'duration': 0},
'Whirligig': {'geyserID': 79, 'loggerID': 22, 'filter_width': 30, 'snr': 3, 'jump_or_max': 'jump', 'jump_window': 6, 'duration': 0}, 
#temperature drops
'Riverside': {'geyserID': 7, 'loggerID': 18, 'filter_width': 60, 'snr': 20, 'jump_or_max': '', 'jump_window': 20, 'duration': 0, 'duration_end_point': 0}
}

params_drops = {
'Depression': {'geyserID': 12, 'loggerID': 8},
}

time_length = 2 * 30 * 24 * 60 * 60 # 2 months at a time for temperature analysis
'''
for geyser in run_these:
    print "Running. . . " + geyser
    p = params[geyser]

    from_time = gtapip.get_latest_etime(p['geyserID']) + 60   
    
    print "Latest E Time: " + str(from_time)
    
    while (from_time <= int(time.time())):
        
        to_time = from_time + time_length
        myLog = pdc.geyser_logger_analyzer(geyser, p['loggerID'], p['geyserID'], int(from_time), int(to_time))

        if (len(myLog.npx) > 60):
            myLog.run_detection(p)
            myLog.post_proposed()
        else:
            print "No temperature data."
        
        #advance from_time
        from_time = to_time
        
#
# One geyser section
#


from_time = '2013-11-06 15:06:00'
final_time =   '2014-06-25 10:00:00'

pattern = '%Y-%m-%d %H:%M:%S'
from_time = int(time.mktime(time.strptime(from_time, pattern)))
final_time = int(time.mktime(time.strptime(final_time, pattern)))

geyser = 'Great Fountain'
p = params[geyser]

while (from_time <= final_time):
        
    to_time = from_time + time_length
    myLog = pdc.geyser_logger_analyzer(geyser, p['loggerID'], p['geyserID'], int(from_time), int(to_time))

    if (len(myLog.npx) > 60):
        myLog.run_detection(p)
        myLog.post_proposed()
    else:
        print "No temperature data."
    
    #advance from_time
    from_time = to_time
'''
########################
#
# Re-adjust already calc'd times
#
########################

# create analyzer and set times
# make a new set of times
# delete old times
# upload new times
geyser = 'Oblong'
p = params[geyser]

propEntries = gtapip.get_proposed_entries(p['geyserID'])

for e in propEntries:
    theTime = e['time']
    
    if theTime > 1398802213:
        window = 30 * 60 #seconds
        from_time = theTime - window / 2
        to_time = theTime + window / 2
        
        #initialize
        myLog = pdc.geyser_logger_analyzer(
                    geyser, 
                    p['loggerID'], 
                    p['geyserID'], 
                    int(from_time), 
                    int(to_time))
        
        idx = len(myLog.npx)
        
        myLog.peaks.append(idx / 2)
        
        myLog.find_biggest_jumps(20)
        myLog.set_proposed_times()

        gtapip.delete_proposed_entry(p['geyserID'], theTime)
        myLog.post_proposed()        
        
        


'''
myLog.plot_series()
#myLog.report(60)
#myLog.post_proposed()

#myLog.optimize()

#myLog.plot_false_positives(6000)
'''