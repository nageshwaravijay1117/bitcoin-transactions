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

class HighValueAddress(Resource):


    def __init__(self):
        super(HighValueAddress, self).__init__()
        
    
    def get(self):
        try:
            output = []
            r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, charset=config.REDIS_CHARSET, decode_responses=True)
            address_set = r.smembers("address")
            for addr in address_set:
                addr_values = r.smembers(addr)
                aggregate_value = 0
                for value in addr_values:
                    key=addr+":"+value
                    if r.get(key) is not None:
                        aggregate_value += int(r.get(key))
                    else:
                        r.srem(addr,key)
                if aggregate_value != 0:
                    output.append({addr:aggregate_value})
                else:
                    r.delete(addr)
                

            return jsonify(data=output, http_status_code=200)

        except Exception as e:
            print(str(e))
            return jsonify(data=str(e), http_status_code=500)



    def options(self):
         pass
