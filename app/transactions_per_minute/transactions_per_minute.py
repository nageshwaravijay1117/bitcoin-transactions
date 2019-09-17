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

class TransactionPerMinute(Resource):


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('min_value',location='args',required=True)
        super(TransactionPerMinute, self).__init__()
        
    
    def get(self):
        try:
            args = self.reqparse.parse_args()
            min_value = args['min_value']
            r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, charset=config.REDIS_CHARSET, decode_responses=True)
            if r.get(min_value) is not None:
                output = r.get(min_value)
            else:
                output="No Data Found for the Provided Time"
            return {min_value :output}

        except Exception as e:
            print(str(e))
            return jsonify(data=str(e), http_status_code=500)



    def options(self):
         pass

class TransactionPerMinuteLastHour(Resource):


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('min_value',location='args',required=True)
        super(TransactionPerMinuteLastHour, self).__init__()
        
    
    def get(self):
        try:
            args = self.reqparse.parse_args()
            min_value = args['min_value']
            hour = int(min_value.split(":")[0])
            minute = int(min_value.split(":")[1])
            print(hour)
            print(minute)
            output = []
            r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, charset=config.REDIS_CHARSET, decode_responses=True)
            for x in range (0,60):
                
                minute+=1
                if minute == 60:
                    minute=0
                    hour = hour+1
                key = str(hour)+":"+str(minute)
                if r.get(key) is not None:
                    output.append({key :r.get(key)})
                else:
                    output.append({key :"No Data Found for the Provided Time"})
            return output
            

        except Exception as e:
            print(str(e))
            return jsonify(data=str(e), http_status_code=500)



    def options(self):
         pass
