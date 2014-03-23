# -*- coding: utf-8 -*-

import requests #for API calls to GeyserTimes.org
import json #API returns JSON

api_str = "http://www.geysertimes.org/api/v2"

def gt_loggerdata(loggerID,epoch_from,epoch_to):

    logger_url = api_str + "/loggerdata/%s/%s/%s" % (loggerID, epoch_from, epoch_to)
    print 'reading: ' + logger_url
    r = requests.get(logger_url)
    log_json = json.loads(r.text)


    log_list = log_json['data']

    x = []
    y = []

    for i in range(0,len(log_list) - 1):
        x.append(log_list[i]['x'])
        y.append(log_list[i]['y'])

    return (x,y)

def gt_entries(geyserID, epoch_from, epoch_to, e_only):
    logger_url = api_str + "/entries/%s/%s/%s" % (geyserID, epoch_from, epoch_to)

    r = requests.get(logger_url)
    r_json = json.loads(r.text)
    
    mylist = r_json['entries']

    data = []

    for i in range(0,len(mylist) - 1):
        if (e_only):
            if (mylist[i]['E'] == 1):
                data.append(mylist[i]['time'])

    return data