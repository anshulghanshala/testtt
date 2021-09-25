import logging
import json
import random

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def makelist(list, slot, start,index):
    temp_list = []
    for i in range(start, slot):
        temp_list.append(list[index])
    return temp_list




def guessNumber(list,slots,data,result,total,start,index):
    if slots > max(total) > start:
        start = max(total)
        index = index + 1
        return makelist(list,slots,start,index)

    if slots > max(total):
        if max(total) == start:
            index = index + 1
            return makelist(list, slots, start, index)





@app.route('/decoder', methods=['POST'])
def evaluatedecoder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    possibleValues = data.get("possible_values")
    slots = data.get("num_slots")
    history = data.get("history")
    history_size = len(history)

    past_data_list = []
    past_data_result =[]
    total = []
    start = 0
    index = 0

    if history_size == 0:
        result = makelist(possibleValues, slots, 0, 0)
        # res = []
        # res.append(result)
        logging.info("My results are :{}".format(result[::]))
        return json.dumps(result)

    else:
        for i in range(len(history)):
            past_data_list.append(i.get("output_received"))
            res = []
            result_data = i.get("result")
            if len(str(result_data)) > 1:
                res = [int(a) for a in str(result_data)]
                total.append(sum(res))
                past_data_result.append(res)
            else:
                res.append(0)
                res.append(result_data)
                total.append(result_data)
                past_data_result.append(res)



    result = {"answer":guessNumber(possibleValues,slots,past_data_list,past_data_result,total,start,index)}
    logging.info("My result :{}".format(result))                                  
    #res = []
    #res.append(result)
    return json.dumps(result) 
    
