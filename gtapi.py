# -*- coding: utf-8 -*-

import requests #for API calls to GeyserTimes.org
import json #API returns JSON


def gt_loggerdata(loggerID,epoch_from,epoch_to):

    logger_url = "http://geysertimes.org/api/v2/loggerdata/%s/%s/%s" % (loggerID, epoch_from, epoch_to)
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

def post_to_geysertimes(geyserID, e_times, elec=1):
    url = "http://localhost/api/v2/submit_entries"
    
    for t in e_times:
        payload = {'geyserID' : geyserID, 'time' : t, 'e' : elec , 'entrantID' : 16}
        r = requests.post(url,data=payload)
        print r.text
