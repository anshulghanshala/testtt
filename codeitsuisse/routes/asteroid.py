import logging
import json

from flask import request, jsonify
from codeitsuisse import app
logger = logging.getLogger(__name__)


def longestPalindrome(s):
    dp = [[False] * len(s) for _ in range(len(s))]
    length: int = 0
    result: str = ''
    st = -1
    en = -1
    for end in range(len(s)):
        for start in range(end + 1):
            if start == end:
                dp[start][end] = True
            elif start + 1 == end:
                dp[start][end] = s[start] == s[end]
            else:
                dp[start][end] = s[start] == s[end] and dp[start + 1][end - 1]

                if dp[start][end] and end - start + 1 > length:
                    length = end - start + 1
                    result = s[start:end + 1]
                    st = start
                    en = end

    return st, en


def count_char(s,st,en):
    if st > 0:
        m = s[st]
        for i in range(st,0,-1):
            if s[i] == m:
                st = st - 1
            else:
                break
    if en < len(s):
        n = s[en]
        for i in range(en,len(s)):
            if s[i] == n:
                en = en + 1
            else:
                break
    return st,en


def total(list):
    total = 0
    for i in list:
        if i <= 6:
            total = total + (i*1)
        if i >= 7:
            total = total + (i*1.5)
        if i >= 10:
            total = total + (i*2)
    return total


def main_work(s):
    st, en = longestPalindrome(s)
    index = (st+en)/2
    if st == en == -1:
        return 1

    st, en = count_char(s, st, en)

    while(1):
        if (st) > 0 and en < len(s)-1:
            st, en = count_char(s, st, en)
        else:
            break

    str = s[st:en]

    res = {}

    for keys in str:
        res[keys] = res.get(keys, 0) + 1
        
    return s , total(res.values()) , index


@app.route('/asteroid', methods=['POST'])
def evaluateasteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("test_cases")
    res = []
    for s in inputValue:
        inp, score,origin = main_work(s)
        result = {
            "input": inp,
            "score": score,
            "origin": origin
        }
        res.append(result)
    
    logging.info("My result :{}".format(res))
    return jsonify(res)
