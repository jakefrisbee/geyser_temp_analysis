# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 17:17:08 2014

@author: Jake
"""
import peak_detection_class as pdc
import gtapi_private as gtapip
import time

params = {
#'Aurum': {'geyserID': 10, 'loggerID': 4, 'filter_width': 60, 'snr': 100, 'jump_or_max': 'max', 'jump_window': 60, 'duration': 0, 'duration_end_point': 0},
#'Beehive': {'geyserID': 1, 'loggerID': 5, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'max', 'jump_window': 300, 'duration': 0, 'duration_end_point': 0},
#'Castle': {'geyserID': 5, 'loggerID': 6, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'max', 'jump_window': 60, 'duration': 0, 'duration_end_point': 0},
#'Daisy': {'geyserID': 4, 'loggerID': 7, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'jump', 'jump_window': 120, 'duration': 0, 'duration_end_point': 0}
#'Grand': {'geyserID': 13, 'loggerID': 10, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'jump', 'jump_window': 240, 'duration': 0, 'duration_end_point': 0},
#'Great Fountain': {'geyserID': 16, 'loggerID': 11, 'filter_width': 60, 'snr': 30, 'jump_or_max': 'max', 'jump_window': 60, 'duration': 0},
#'Lion': {'geyserID': 14, 'loggerID': 13, 'filter_width': 60, 'snr': 25, 'jump_or_max': 'max', 'jump_window': 10, 'duration': 0, 'duration_end_point': 0},
#'Little Squirt': {'geyserID': 36, 'loggerID': 14, 'filter_width': 60, 'snr': 10, 'jump_or_max': 'max', 'jump_window': 10, 'duration': 0, 'duration_end_point': 0},
#'Oblong': {'geyserID': 23, 'loggerID': 15, 'filter_width': 60, 'snr': 15, 'jump_or_max': 'max', 'jump_window': 120, 'duration': 0, 'duration_end_point': 0},
#'Old Faithful': {'geyserID': 2, 'loggerID': 16, 'filter_width': 90, 'snr': 20, 'jump_or_max': 'max', 'jump_window': 30, 'duration': 0, 'duration_end_point': 0},
#'Plume': {'geyserID': 3, 'loggerID': 17, 'filter_width': 60, 'snr': 100, 'jump_or_max': 'max', 'jump_window': 10, 'duration': 0, 'duration_end_point': 0},
#'Turban': {'geyserID': 28, 'loggerID': 20, 'filter_width': 60, 'snr': 100, 'jump_or_max': 'max', 'jump_window': 10, 'duration': 0, 'duration_end_point': 0},
#duration
#'Artemisia': {'geyserID': 19, 'loggerID': 3, 'filter_width': 60, 'snr': 100, 'jump_or_max': 'jump', 'jump_window': 300, 'duration': 1, 'duration_end_point': 0},
#'Fountain': {'geyserID': 15, 'loggerID': 9, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'first_jump', 'jump_window': 120, 'duration': 1, 'duration_end_point': 2},
'Grotto': {'geyserID': 21, 'loggerID': 12, 'filter_width': 60, 'snr': 50, 'jump_or_max': 'first_jump', 'jump_window': 120, 
           'duration': { 'duration_end_point': 2, 
                        'decrease_length': 20, # # of points to look for decreasing temperatures
                        'decrease_count_threshold': 20, # # of points that must be decreasing
                        'look_ahead': 2000, # points into the future to look for temperature dropoff
                        }
           }
#'Spouter': {'geyserID': 50, 'loggerID': 19, 'filter_width': 60, 'snr': 100, 'jump_or_max': 'max', 'jump_window': 30, 'duration': 1, 'duration_end_point': 0},
#YVO
#'Echinus': {'geyserID': 81, 'loggerID': 23, 'filter_width': 30, 'snr': 50, 'jump_or_max': 'max', 'jump_window': 300, 'duration': 0},
#'Steamboat': {'geyserID': 163, 'loggerID': 21, 'filter_width': 30, 'snr': 50, 'jump_or_max': 'max', 'jump_window': 300, 'duration': 0},
#'Whirligig': {'geyserID': 79, 'loggerID': 22, 'filter_width': 30, 'snr': 3, 'jump_or_max': 'jump', 'jump_window': 6, 'duration': 0}, 
#temperature drops
#'Riverside': {'geyserID': 7, 'loggerID': 18, 'filter_width': 60, 'snr': 20, 'jump_or_max': '', 'jump_window': 20, 'duration': 0, 'duration_end_point': 0}
}

params_drops = {
'Depression': {'geyserID': 12, 'loggerID': 8},
}

time_length = 2 * 30 * 24 * 60 * 60 # 2 months at a time for temperature analysis

for geyser in params:
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
        


'''
from_time = '2012-11-06 11:00:00'
to_time =   '2012-12-01 00:00:00'


myLog.plot_series()
#myLog.report(60)
#myLog.post_proposed()

#myLog.optimize()

#myLog.plot_false_positives(6000)
'''