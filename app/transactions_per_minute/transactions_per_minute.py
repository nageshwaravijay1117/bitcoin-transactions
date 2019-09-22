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
import csv
import json
from flask_restful import reqparse
import re
from datetime import datetime
import redis


class TransactionPerMinute(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('min_value', location='args', required=True)
        super(TransactionPerMinute, self).__init__()

    def get(self):
        try:
            args = self.reqparse.parse_args()
            min_value = args['min_value']
            # Connecting to Redis Database
            r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT,
                                  charset=config.REDIS_CHARSET, decode_responses=True)
            # Getting the detail for the given Time Value
            if r.get(min_value) is not None:
                output = r.get(min_value)
            else:
                output = "No Data Found for the Provided Time"
            return {min_value: output}

        except Exception as e:
            print(str(e))
            return jsonify(data=str(e), http_status_code=500)

    def options(self):
        pass


class TransactionPerMinuteLastHour(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('min_value', location='args', required=True)
        super(TransactionPerMinuteLastHour, self).__init__()

    def get(self):
        try:
            args = self.reqparse.parse_args()
            min_value = args['min_value']
            hour = int(min_value.split(":")[0])
            minute = int(min_value.split(":")[1])
            output = []
            # Connecting to Redis Database
            r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT,
                                  charset=config.REDIS_CHARSET, decode_responses=True)
            # Getting the detail for the the last hour
            for x in range(0, 60):
                minute += 1
                if minute == 60:
                    minute = 0
                    hour = hour+1
                key = str(hour)+":"+str(minute)
                if r.get(key) is not None:
                    output.append({key: r.get(key)})
                else:
                    output.append({key: "No Data Found for the Provided Time"})
            return output

        except Exception as e:
            print(str(e))
            return jsonify(data=str(e), http_status_code=500)

    def options(self):
        pass
