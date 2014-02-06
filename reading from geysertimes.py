# -*- coding: utf-8 -*-

import urllib2 #for API calls to GeyserTimes.org
import json #API returns JSON

gt_loggerdata(22,1371570056,1391570056)

def gt_loggerdata(loggerID,epoch_from,epoch_to):

    logger_url = "http://localhost/api/v2/loggerdata/%s/%s/%s" % (loggerID, epoch_from, epoch_to)
    content = urllib2.urlopen(logger_url).read()
    log_json = json.loads(content)

    log_list = log_json['data']

    x = []
    y = []

    for i in range(0,len(log_list) - 1):
        x.append(log_list[i]['x'])
        y.append(log_list[i]['y'])
    
    plot(y)
