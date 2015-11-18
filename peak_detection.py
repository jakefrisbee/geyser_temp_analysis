# -*- coding: utf-8 -*-

import numpy as np
import scipy
import scipy.signal

def smooth(x,window_len=11,window='hanning'):
#    smooth the data using a window with requested size.
#    
#    This method is based on the convolution of a scaled window with the signal.
#    The signal is prepared by introducing reflected copies of the signal 
#    (with the window size) in both ends so that transient parts are minimized
#    in the begining and end part of the output signal.
#    
#    input:
#        x: the input signal 
#        window_len: the dimension of the smoothing window; should be an odd integer
#        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
#            flat window will produce a moving average smoothing.
#
#    output:
#        the smoothed signal
#        
#    example:
#
#    t=linspace(-2,2,0.1)
#    x=sin(t)+randn(len(t))*0.1
#    y=smooth(x)
#    
#    see also: 
#    
#    np.hanning, np.hamming, np.bartlett, np.blackman, np.convolve
#    scipy.signal.lfilter
# 
#    TODO: the window parameter could be the window itself if an array instead of a string
#    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.

    if x.ndim != 1:
        raise(ValueError, "smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise(ValueError, "Input vector needs to be bigger than window size.")


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise(ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y
    


def temperature_csv_to_temperature_array(fname):
    data_types = [('i6'),('S8'),('S8'),('f6')]
    data = np.genfromtxt(fname,delimiter=",",skip_header=1,dtype=data_types)
    
    return data
    
def extract_temperature_array(data):
    t = data[:,[3]]
    return np.squeeze(np.asarray(t))

def smooth_temperature(vector,filter_width=15):
    v_smooth = smooth(vector,filter_width,'flat')
    v_smooth = v_smooth[0:len(vector)]
    v = vector - v_smooth
    
    return v

def find_geyser_peaks(v,snr=10):
    
    peaks = scipy.signal.find_peaks_cwt(v,np.arange(1,10),min_snr=snr)
    
    return peaks

def find_biggest_jumps(temps,guesses,window=6):
    final = []
    for i in guesses:
        theArea = temps[max(0,i-window/2):min(len(temps)-1,i+window/2)]
        jumps = []
        for j in range(1,len(theArea)):
            jumps.append(theArea[j] - theArea[j-1])
        
        if (len(jumps) > 0):
            npj = np.asarray(jumps)
            max_index = i - window/2 + npj.argmax() + 1
            final.append(max_index)
        
        #remove duplicate indexes
        final = remove_duplicates(final)
        
    return final
    
def eruption_times(peak_list,csv_array):
    e = []
    for i in peak_list:
        e.append(csv_array[i][1] + ' ' + csv_array[i][2])
    
    return e
    
#remove duplicates
def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def times_and_intervals(indexes,times):
    final = []
    e_times = []
    intervals = []
    for i in indexes:
        if (i < len(times)):
            e_times.append(times[i])
        
    for i in range(1,len(e_times)):
        intervals.append(e_times[i] - e_times[i-1])
    
    final = zip(indexes, e_times,intervals)    
    
    return final



