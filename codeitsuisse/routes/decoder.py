#import logging
#import json
#import random
#
#from flask import request, jsonify
#
#from codeitsuisse import app
#
#logger = logging.getLogger(__name__)
#
#
#def makelist(list, slot, start,index):
#    temp_list = []
#    for i in range(start, slot):
#        temp_list.append(list[index])
#    return temp_list
#
#
#
#
#def guessNumber(list,slots,data,result,total,start,index):
#    if slots > max(total) > start:
#        start = max(total)
#        index = index + 1
#        return makelist(list,slots,start,index)
#
#    if slots > max(total):
#        if max(total) == start:
#            index = index + 1
#            return makelist(list, slots, start, index)
#
#
#
#
#
#@app.route('/decoder', methods=['POST'])
#def evaluatedecoder():
#    data = request.get_json()
#    logging.info("data sent for evaluation {}".format(data))
#    possibleValues = data.get("possible_values")
#    slots = data.get("num_slots")
#    history = data.get("history")
#    history_size = len(history)
#
#    past_data_list = []
#    past_data_result =[]
#    total = []
#    start = 0
#    index = 0
#
#    if history_size == 0:
#        result = {"answer":makelist(possibleValues, slots, 0, 0)}
#        # res = []
#        # res.append(result)
#        logging.info("My results are :{}".format(result))
#        return json.dumps(result)
#
#    else:
#        for i in range(len(history)):
#            past_data_list.append(i.get("output_received"))
#            res = []
#            result_data = i.get("result")
#            if len(str(result_data)) > 1:
#                res = [int(a) for a in str(result_data)]
#                total.append(sum(res))
#                past_data_result.append(res)
#            else:
#                res.append(0)
#                res.append(result_data)
#                total.append(result_data)
#                past_data_result.append(res)
#
#
#
#    result = {"answer":guessNumber(possibleValues,slots,past_data_list,past_data_result,total,start,index)}
#    logging.info("My result :{}".format(result))
#    #res = []
#    #res.append(result)
#    return json.dumps(result)
    
import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def make_list(lists, slot, start, index):
    temp_list = []
    for i in range(start, slot):
        temp_list.append(lists[index])
    return temp_list


def shuffle(data, number, slots):
    x = 0
    y = 1
    if slots == number:
        number = number - 1

    for i in range(number):
        data[x], data[y] = data[y], data[x]
        x = x + 1
        y = y + 1
    return data

def most_frequent(my_list):
    return max(set(my_list), key = my_list.count)


def right_combination(slots, data, result, total):
    new_data = []
    new_result = []
    indices = [i for i, x in enumerate(total) if x == slots]
    for i in indices:
        new_data.append(data[i])
        new_result.append(result[i])

    if len(indices) == 1:
        return shuffle(new_data, new_result[0][0],slots)


def guess_number(lists, slots, data, result, total, start, index):
    if slots > max(total) > start:
        start = max(total)
        index = index + 1
        return make_list(lists, slots, start, index)

    if slots > max(total):
        if max(total) == start:
            index = index + 1
            return make_list(lists, slots, start, index)

    if slots == max(total):
        return right_combination(lists, slots, data, result, total)


@app.route('/decoder', methods=['POST'])
def evaluatedecoder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    possibleValues = data.get("possible_values")
    slots = data.get("num_slots")
    history = data.get("history")
    history_size = len(history)

    past_data_list = []
    past_data_result = []
    total = []
    start = 0
    index = 0

    if history_size == 0:
        result = {"answer": make_list(possibleValues, slots, 0, 0)}
#        res = []
#        res.append(result)
        logging.info("My result :{}".format(result))
        return jsonify(result)

    else:
        for i in history:
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
