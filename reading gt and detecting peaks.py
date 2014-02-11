# -*- coding: utf-8 -*-
"""
Created on Wed Feb 05 12:01:19 2014

@author: Jake
"""

import gtapi
import peak_detection as pd
x = []
y = []

params = {'Whirligig': {'geyserID': 79, 'loggerID': 22, 'filter_width': 30, 'snr': 3, 'jump_window': 6},
          'Aurum': {'geyserID': x, 'loggerID': 10, 'filter_width': 60, 'snr': 100, 'jump_window': 30},
          'Plume': {'geyserID': x, 'loggerID': 17, 'filter_width': 60, 'snr': 100, 'jump_window': 10},
          #'Little Squirt': {'geyserID': x, 'loggerID': 14, 'filter_width': 60, 'snr': 10, 'jump_window': 10},
          'Lion': {'geyserID': x, 'loggerID': 13, 'filter_width': 60, 'snr': 25, 'jump_window': 10},
          'Beehive': {'geyserID': x, 'loggerID': 5, 'filter_width': 60, 'snr': 50, 'jump_window': 30}
}

geyser = 'Beehive'
from_time = 1321917378
to_time =   1323927378


p = params[geyser]



#get temperature data: x is epoch time, y is temperature
#x, y = gtapi.gt_loggerdata(22,1384515512,1386115206)
x, y = gtapi.gt_loggerdata(p['loggerID'],from_time,to_time)

#convert to numpy array
npy = np.asarray(y)
npx = np.asarray(x)

#smooth the time series
smoo = pd.smooth_temperature(npy, p['filter_width'])

#find peaks
all_peaks = pd.find_geyser_peaks(smoo, p['snr'])

#find biggest temperature jump near peaks   
t = pd.find_biggest_jumps(npy,all_peaks, p['jump_window'])

def plot_peaks(x,y,indexes):
    clf()
    plot(x,y)
    
    for i in indexes:
        plot(x[i],60,'r+')
    

with_intervals = times_and_intervals(t,npx)

e_times = [item[1] for item in with_intervals]

plot_peaks(npx,npy,t)
    
#gtapi.post_to_geysertimes(p['geyserId'],e_times)    


#show longest and shortest intervals
#plot(npy[t[0]-5:t[2]+5])
#send to GT (need API)