# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 15:49:07 2014

@author: Jake
"""
import time
import numpy as np

class geyser_logger_analyzer:
    import gtapi as gtapi
    import gtapi_private as gtp
    import peak_detection as pd
    import scipy
    import scipy.signal as sig
    
    
    
    def __init__(self, loggerID, geyserID, from_time, to_time):
        self.loggerID = loggerID
        self.geyserID = geyserID
        
        if(isinstance(from_time, int)): #accept unixtime
            self.from_time = from_time
            self.to_time = to_time
        else:
            self.from_time = int(time.mktime(time.strptime(from_time,'%Y-%m-%d %H:%M:%S')))
            self.to_time = int(time.mktime(time.strptime(to_time,'%Y-%m-%d %H:%M:%S')))
        
        #get temperature data: x is epoch time, y is temperature
        x, y = self.gtapi.gt_loggerdata(self.loggerID,self.from_time,self.to_time)
        self.actual_times = self.gtapi.gt_entries(self.geyserID,self.from_time,self.to_time, 1)
        #convert to numpy array
        self.npy = np.asarray(y)
        self.npx = np.asarray(x)
    
    def smooth_temperature(self, filter_width=15):
        v_smooth = self.pd.smooth(self.npy,filter_width,'flat')
        v_smooth = v_smooth[0:len(self.npy)]
        self.smoothed_temp = self.npy - v_smooth
        
    def find_peaks(self, snr=10):
        self.peaks = self.sig.find_peaks_cwt(self.smoothed_temp,np.arange(1,10),min_snr=snr)
    
    def find_biggest_jumps(self, window=6):
        final = []
        for i in self.peaks:
            theArea = self.npy[max(0,i-window/2):min(len(self.npy)-1,i+window/2)]
            jumps = []
            for j in range(1,len(theArea)):
                jumps.append(theArea[j] - theArea[j-1])
            
            if (len(jumps) > 0):
                npj = np.asarray(jumps)
                max_index = i - window/2 + npj.argmax() + 1
                final.append(max_index)
            
        self.big_jumps = remove_duplicates(final)
    
    def set_proposed_times(self):
        self.proposed_times = []
        self.proposed_intervals = []
        self.proposed_indexes = []
        
        for i in self.big_jumps:
            if (i < len(self.npx)):
                self.proposed_times.append(self.npx[i])
                self.proposed_indexes.append(i)
            
        for i in range(1,len(self.proposed_times)):
            self.proposed_intervals.append(self.proposed_times[i] - self.proposed_times[i-1])
           
        
    def run_detection(self, filter_width, snr, jump_or_max, jump_window, b_durations):
        print "smoothing temperature at %s" % filter_width
        self.smooth_temperature(filter_width)
        print "finding peaks, snr: %s" % snr
        self.find_peaks(snr)
        if (jump_or_max == 'jump'):
            print "locating biggest jump within %s" % jump_window
            self.find_biggest_jumps(jump_window)
        else:
            print "finding local max within %s" % jump_window
            self.find_local_max(jump_window)
        print "setting proposed times"
        self.set_proposed_times()
        if (b_durations):
            print "finding durations"
            self.find_durations()
                 
    def find_durations(self):
        self.durations = []
        decrease_length = 20 # # of points to look for decreasing temperatures
        look_ahead = 500 # points into the future to look for temperature dropoff
        #find first time that X points are all decreasing
        #find inflection point
        #subtract time from proposed_time / 60 for duration
        for i in self.proposed_indexes:
            dur = self.find_end_time(i, decrease_length, look_ahead)
            self.durations.append(dur)
            
    def find_end_time(self, idx_start, decrease_length, look_ahead):
        duration = 0 #default
        for j in range(0,look_ahead): #how far out we go to find decreases
        #section to analyze
            d = self.npy[idx_start+j:idx_start+j+decrease_length]
            dd = diff(d)
            if (max(dd) < 0): #then it's all decreasing
                #find inflection point
                #where differences go from - to +
                ddd = diff(dd)
                for z in range(0,len(ddd) - 1):
                    if (ddd[z] <= 0 and ddd[z+1] >=0):
                        end_idx = idx_start + j + z
                        end = self.npx[end_idx]
                        duration = (end - self.npx[idx_start]) / 60
                        return duration
        
    def report(self, sec_tolerance):
        #loop thru calc, find matches
        #find true positive
        #find false positive
        #find false negative
        self.true_positive = []
        self.false_positive = []
        self.missed = []
    
        for i in range(0, len(self.proposed_times)):
            calc_time = self.proposed_times[i]
            closest_actual = min(self.actual_times, key=lambda x:abs(x-calc_time))
            dist = abs(closest_actual - calc_time)
            if dist < sec_tolerance:
                self.true_positive.append(calc_time)
            else:
                self.false_positive.append(calc_time)
                
        for i in range(0, len(self.actual_times)):
            a_time = self.actual_times[i]
            closest_calc = min(self.proposed_times, key=lambda x:abs(x-a_time))
            dist = abs(closest_calc - a_time)
            if dist > sec_tolerance:
                self.missed.append(a_time)
        
        print "Total Calc Times: %s" % len(self.proposed_times)
        print "True positives: %s" % len(self.true_positive)
        print "False positives: %s" % len(self.false_positive)
        print "Actual eruptions: %s" % len(self.actual_times)
        print "Missed eruptions: %s" % len(self.missed)
        
        self.results = {"calc": len(self.proposed_times), 
                        "actual": len(self.actual_times), 
                        "true": len(self.true_positive), 
                        "false": len(self.false_positive), 
                        "missed": len(self.missed)}
    
    def plot_false_positives(self, plot_window = 60):
        clf()        
        for i in self.false_positive:
            idx = np.where(self.npx == i)
            idx = idx[0][0]
            
            figure("False +: " + str(i))
            plot(x[idx-plot_window:idx+plot_window], y[idx-plot_window:idx+plot_window])
            
    def plot_series(self):
        clf()
        plot(self.npx,self.npy)
    
        for i in self.proposed_indexes:
            plot(self.npx[i],60,'r+')

    def optimize(self):
        self.report_array = {}
        
        filter_width = [30, 120, 240, 360, 480, 600]
        snr = [5, 25, 50, 100]
        jump_window = [30]
        seconds_tolerance = 120 
        
        for f in filter_width:
            for s in snr:
                for j in jump_window:
                    print "Running: filter %s; snr %s; jump %s" % (f, s, j)
                    self.run_detection(f, s, j)
                    self.report(seconds_tolerance)
                    self.report_array.update({
                        "geyserID": self.geyserID,
                        "loggerID": self.loggerID,
                        "from": self.from_time,
                        "to": self.to_time,
                        "filter_width": f,
                        "snr": s,
                        "jump_window": j,
                        "actuals": len(self.actual_times),
                        "found": len(self.proposed_times), 
                        "true": len(self.true_positive), 
                        "false": len(self.false_positive), 
                        "missed": len(self.missed)
                        })
                    
        print self.report_array
        
    def post_proposed(self):
        self.gtp.post_to_geysertimes(self.geyserID,self.proposed_times)
        
# misc functions
def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
    


