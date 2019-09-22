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
import redis


class HighValueAddress(Resource):

    def __init__(self):
        super(HighValueAddress, self).__init__()

    def get(self):
        try:
            output = []
            # Connecting to Redis Database
            r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT,
                                  charset=config.REDIS_CHARSET, decode_responses=True)
            # Getting All the Address as Set
            address_set = r.smembers("address")
            for addr in address_set:
                # Getting All the Index of the current Address as Set
                addr_values = r.smembers(addr)
                aggregate_value = 0
                # Adding all the values of the particular address list
                for value in addr_values:
                    key = addr+":"+value
                    if r.get(key) is not None:
                        aggregate_value += int(r.get(key))
                    else:
                        r.srem(addr, key)
                if aggregate_value != 0:
                    output.append({addr: aggregate_value})
                else:
                    r.delete(addr)
                    r.srem("address", addr)

            return jsonify(data=output, http_status_code=200)

        except Exception as e:
            print(str(e))
            return jsonify(data=str(e), http_status_code=500)

    def options(self):
        pass
