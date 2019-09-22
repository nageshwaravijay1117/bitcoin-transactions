"""
==========================================
Author:Nageshwara Vijay
Created-At:15-09-2019
Last-Modified:17-09-2019
==========================================
"""
import config
from flask import jsonify
import requests
from flask_restful import Resource
import csv, json
from flask_restful import reqparse
import re
import redis

class Transaction(Resource):


    def __init__(self):
        super(Transaction, self).__init__()
        
    
    def get(self):
        try:
            output = []
            #Connecting to Redis Database
            r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, charset=config.REDIS_CHARSET, decode_responses=True)
            #Geeting List of ALL Transactions
            transaction_list = r.smembers("transaction")
            #Geeting Last Index of Transactions
            curr_index = int(r.get("transaction_index"))
            #Checking for Transaction Limit Exceeded and the Index Value is Reset or Not
            if not (1800000 in transaction_list):
                #Getting the last 100 Transactions
                for x in range(0, 100):
                    key = 'transaction'+str(curr_index - x)
                    output.append(r.get(key))
            else:
                tmp = curr_index
                for x in range(0, 100):
                    if (curr_index - x) >= 1:
                        key = 'transaction'+str(curr_index - x)
                    else:
                        key = 'transaction'+str(1800000 + tmp - x)
                    output.append(r.get(key))

            return jsonify(data=output, http_status_code=200)

        except Exception as e:
            print(str(e))
            return jsonify(data=str(e), http_status_code=500)



    def options(self):
         pass
