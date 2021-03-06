# -*- coding: utf-8 -*-

import requests #for API calls to GeyserTimes.org
import json #API returns JSON


def gt_loggerdata(loggerID,epoch_from,epoch_to):

    logger_url = "http://geysertimes.org/api/v2/loggerdata/%s/%s/%s" % (loggerID, epoch_from, epoch_to)
    content = requests.get(logger_url)
    log_json = json.loads(content)

    log_list = log_json['data']

    x = []
    y = []

    for i in range(0,len(log_list) - 1):
        x.append(log_list[i]['x'])
        y.append(log_list[i]['y'])

    return (x,y)
