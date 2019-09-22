"""
==========================================
Author:Nageshwara Vijay
Created-At:15-09-2019
Last-Modified:17-09-2019
==========================================
"""

import json
from confluent_kafka import Consumer, KafkaError
from websocket import create_connection
from datetime import datetime
import redis


class MyClass:
    def __init__(self):

    curr_time = ''
    prev_time = '00:00'
    count = 0
    r = redis.StrictRedis(host="localhost", port=6379,
                          charset="utf-8", decode_responses=True)

    def start_streaming():
        settings = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'mygroup',
            'client.id': 'client-1',
            'enable.auto.commit': True,
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'}}
        # Connecting to kafka Producer
        c = Consumer(settings)

        c.subscribe(['mytopic'])
        try:
            while True:
                msg = c.poll(0.1)
                if msg is None:
                    continue
                elif not msg.error():

                    MyClass.calculate_transaction_per_minute(
                        json.loads(msg.value()))
                    MyClass.save_out_addr_value(json.loads(msg.value()))
                    MyClass.save_each_value(json.loads(msg.value()))
                else:
                    print('Error occured: {0}'.format(msg.error().str()))
        except Exception as e:
            pass
        finally:
            c.close()

    # Calculate transactions per minute and store it in redis DB

    def calculate_transaction_per_minute(data_decoded):
        try:

            tmp_date = data_decoded['x']['time']
            time_of_tran = datetime.utcfromtimestamp(
                int(tmp_date)).strftime('%Y-%m-%d %H:%M:%S')
            time_splited = time_of_tran.split()

            MyClass.count += 1
            MyClass.curr_time = time_splited[1][:5]
            if time_splited[1][6:] == '00' or time_splited[1][6:] == '01':

                if MyClass.prev_time != MyClass.curr_time:
                    MyClass.prev_time = MyClass.curr_time
                    if MyClass.r.get(str(MyClass.curr_time)) is not None:
                        tmp_count = MyClass.r.get(str(MyClass.curr_time))
                        MyClass.r.set(str(MyClass.curr_time),
                                      MyClass.count+tmp_count)
                        MyClass.r.expire(str(MyClass.curr_time), 10800)

                    else:
                        MyClass.r.set(str(MyClass.curr_time), MyClass.count)
                        MyClass.r.expire(str(MyClass.curr_time), 10800)
                    MyClass.curr_time = time_splited[1][:5]
                    MyClass.count = 0

        except Exception as e:
            print(str(e))

    def save_out_addr_value(data_decoded):
        try:
            output_list = data_decoded['x']['out']
            for output in output_list:
                if output['addr'] is not None:

                    if len(MyClass.r.smembers(output['addr'])) != 0:
                        MyClass.r.sadd('address', output['addr'])
                        addr_array = MyClass.r.smembers(output['addr'])
                        index = max(set(map(int, addr_array)))+1

                        MyClass.r.sadd(output['addr'], int(index))
                        key = output['addr']+':'+str(index)
                        MyClass.r.set(key, output['value'])
                        MyClass.r.expire(str(key), 10800)
                    else:
                        MyClass.r.sadd(output['addr'], int(1))
                        key = output['addr']+':'+str(1)
                        MyClass.r.expire(str(key), 10800)
        except Exception as e:
            print(str(e))

    def save_each_value(data_decoded):
        try:

            output = data_decoded['x']
            output['updated_at'] = str(datetime.now())
            if len(MyClass.r.smembers('transaction')) != 0:
                tran_array = MyClass.r.smembers('transaction')
                index = int(MyClass.r.get('transaction_index'))+1
                if(index > 1800000):
                    index = 1
                MyClass.r.set('transaction_index', index)
                MyClass.r.sadd('transaction', index)
                key = 'transaction'+str(index)
                MyClass.r.set(key, str(output))
                MyClass.r.expire(str(key), 10800)
            else:

                MyClass.r.sadd('transaction', 1)
                key = 'transaction'+str(1)
                MyClass.r.set('transaction_index', 1)
                MyClass.r.set(key, str(output))
                MyClass.r.expire(str(key), 10800)
        except Exception as e:
            print(str(e))


MyClass.start_streaming()
