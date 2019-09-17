import config
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from flask import jsonify
import requests
from flask_restful import Resource
import csv, json
from requests.auth import HTTPBasicAuth
from flask_restful import reqparse
import re
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import redis

class Transaction(Resource):


    def __init__(self):
        super(Transaction, self).__init__()
        
    
    def get(self):
        try:
            output = []
            r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, charset=config.REDIS_CHARSET, decode_responses=True)
            transaction_list = r.smembers("transaction")
            curr_index = int(r.get("transaction_index"))
            print(transaction_list)
            if not (1800000 in transaction_list):
                print('current index',curr_index)
                for x in range(0, 100):
                    print('current index',curr_index)
                    key = 'transaction'+str(curr_index - x)
                    print(key)
                    output.append(r.get(key))
            else:
                tmp = curr_index
                for x in range(0, 100):
                    print('current index',curr_index)
                    if (curr_index - x) >= 1:
                        key = 'transaction'+str(curr_index - x)
                    else:
                        key = 'transaction'+str(1800000 + tmp - x)
                    print(key)
                    output.append(r.get(key))

            return jsonify(data=output, http_status_code=200)

        except Exception as e:
            print(str(e))
            return jsonify(data=str(e), http_status_code=500)



    def options(self):
         pass
