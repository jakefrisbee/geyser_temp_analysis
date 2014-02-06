# -*- coding: utf-8 -*-
"""
Created on Wed Feb 05 12:01:19 2014

@author: Jake
"""
import requests

import gtlogger as gtl
import peak_detection as pd
x = []
y = []

params = {{geyser: 'Whirligig', geyserID: 79, loggerID: 22, snr=5, jump_window=6}}

#get temperature data: x is epoch time, y is temperature
x, y = gtl.gt_loggerdata(22,1374515512,1386115206)

#convert to numpy array
npy = np.asarray(y)
npx = np.asarray(x)

#smooth the time series
smoo = pd.smooth_temperature(npy)

#find peaks
all_peaks = pd.find_geyser_peaks(smoo,snr=5)

#find biggest temperature jump near peaks   
t = pd.find_biggest_jumps(npy,all_peaks)

def plot_peaks(x,y,indexes):
    clf()
    plot(x,y)
    
    for i in indexes:
        plot(x[i],60,'r+')
    

with_intervals = times_and_intervals(t,npx)

e_times = [item[1] for item in with_intervals]

plot_peaks(npx,npy,t)


def post_to_geysertimes(geyserID, e_times, elec=1):
    url = "http://localhost/api/v2/submit_entries"
    
    for t in e_times:
        payload = {'geyserID' : geyserID, 'time' : t, 'e' : elec , 'entrantID' : 16}
        r = requests.post(url,data=payload)
        print r.text
    
post_to_geysertimes(79,e_times)    
    
#show longest and shortest intervals
#plot(npy[t[0]-5:t[2]+5])
#send to GT (need API)