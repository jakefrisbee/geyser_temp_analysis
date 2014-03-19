# -*- coding: utf-8 -*-
"""
Created on Wed Feb 05 12:01:19 2014

@author: Jake
"""

import gtapi
import peak_detection as pd
import gtapi_private as gtapip

x = []
y = []

params = {'Whirligig': {'geyserID': 79, 'loggerID': 22, 'filter_width': 30, 'snr': 3, 'jump_window': 6},
          'Aurum': {'geyserID': 10, 'loggerID': 4, 'filter_width': 60, 'snr': 100, 'jump_window': 30},
          'Plume': {'geyserID': x, 'loggerID': 17, 'filter_width': 60, 'snr': 100, 'jump_window': 10},
          #'Little Squirt': {'geyserID': x, 'loggerID': 14, 'filter_width': 60, 'snr': 10, 'jump_window': 10},
          'Lion': {'geyserID': x, 'loggerID': 13, 'filter_width': 60, 'snr': 25, 'jump_window': 10},
          'Beehive': {'geyserID': 1, 'loggerID': 5, 'filter_width': 60, 'snr': 50, 'jump_window': 30},
          'Old Faithful': {'geyserID': 2, 'loggerID': 16, 'filter_width': 60, 'snr': 50, 'jump_window': 30}

}

geyser = 'Aurum'
from_unix = 1352314261
to_unix =   1353414261

p = params[geyser]

#get temperature data: x is epoch time, y is temperature
x, y = gtapi.gt_loggerdata(4,from_unix,to_unix)
actual_times = gtapi.gt_entries(10,from_unix,to_unix, 1)
#convert to numpy array
npy = np.asarray(y)
npx = np.asarray(x)  



def big_loop(loggerID, geyserID, from_time, to_time):
    filter_width = [120]#, 240, 360, 480, 600]
    snr = [100]
    jump_window = [30]
    seconds_tolerance = 120
    
    #get temperature data: x is epoch time, y is temperature
    x, y = gtapi.gt_loggerdata(loggerID,from_time,to_time)
    actual_times = gtapi.gt_entries(geyserID,from_time,to_time, 1)
    #convert to numpy array
    npy = np.asarray(y)
    npx = np.asarray(x)  
    
    for f in filter_width:
        for s in snr:
            for j in jump_window:
                result = peak_detect(npx, npy, actual_times, seconds_tolerance, f, s, j)
                print f, s, j, result

def peak_detect(npx, npy, actual_times, tolerance, filter_width, snr, jump_window):
    
    #smooth the time series
    smoo = pd.smooth_temperature(npy, filter_width)
    
    #find peaks
    all_peaks = pd.find_geyser_peaks(smoo, snr)
    
    #find biggest temperature jump near peaks   
    t = pd.find_biggest_jumps(npy, all_peaks, jump_window)     
    
    with_intervals = pd.times_and_intervals(t,npx)
    
    e_times = [item[1] for item in with_intervals]
    
    #plot_peaks(npx,npy,t)
    
    result = compare_calc_times_to_actual(e_times, actual_times, tolerance)
    return result
        
def plot_peaks(x,y,indexes):
    clf()
    plot(x,y)
    
    for i in indexes:
        plot(x[i],60,'r+')

def plot_at_time(x,y,time,plot_window=60):
    i = np.where(x == time)
    i = i[0][0]
    clf()
    plot(x[i-plot_window:i+plot_window], y[i-plot_window:i+plot_window])
            
def compare_calc_times_to_actual(calc, actual, sec_tolerance):
    #loop thru calc, find matches
    #find true positive
    #find false positive
    #find false negative
    true_positive = []
    false_positive = []
    missed = []

    for i in range(0, len(calc)):
        calc_time = calc[i]
        closest_actual = min(actual, key=lambda x:abs(x-calc_time))
        dist = abs(closest_actual - calc_time)
        if dist < sec_tolerance:
            true_positive.append(calc_time)
        else:
            false_positive.append(calc_time)
            
    for i in range(0, len(actual)):
        closest_calc = min(calc, key=lambda x:abs(x-actual[i]))
        dist = abs(closest_calc - actual[i])
        if dist > sec_tolerance:
            missed.append(actual[i])
    '''
    print "Total Calc Times: %s" % len(calc)
    print "True positives: %s" % len(true_positive)
    print "False positives: %s" % len(false_positive)
    print "Actual eruptions: %s" % len(actual)
    print "Missed eruptions: %s" % len(missed)
    '''
    results = {"calc": len(calc), "actual": len(actual), "true": len(true_positive), "false": len(false_positive), "missed": len(missed)}

    print false_positive
    
    return results
  
#plot_at_time(npx,npy,1353384061)  
big_loop(4,10,from_unix,to_unix)

    
gtapip.post_to_geysertimes(p['geyserID'],e_times)