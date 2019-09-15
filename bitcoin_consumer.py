from confluent_kafka import Consumer, KafkaError
from websocket import create_connection
from datetime import datetime
import redis
import json



settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'client.id': 'client-1',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}

r = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

c = Consumer(settings)

c.subscribe(['mytopic'])
currTime = ''
prev_time = '00:00'
count =0
dataList =[]
try:
    while True:
        msg = c.poll(0.1)
        if msg is None:
            continue
        elif not msg.error():
            print('Received message: {0}'.format(msg.value()))
            data_decoded=json.loads(msg.value())
            hash=data_decoded['x'] 
            tmpDate=data_decoded['x']['time'] 
            timeOfTran=datetime.utcfromtimestamp(int(tmpDate)).strftime('%Y-%m-%d %H:%M:%S') 
            timeSplited= timeOfTran.split() 
            print('\n ',timeSplited[6:]) 
            count+=1 
            currTime = timeSplited[1][:5] 
            if timeSplited[1][6:] == '00' or timeSplited[1][6:] == '01':
                print('asd') 
                if prev_time != currTime:
                    prev_time = currTime
                    if r.get(str(currTime)) is not None:
                        tmp_count = r.get(str(currTime))
                        r.set(str(currTime),count+tmp_count)
                        r.expire(str(currTime),10800)
                        
                    else:
                        r.set(str(currTime),count)
                        r.expire(str(currTime),10800)
                    dataList.append({currTime:count}) 
                    currTime = timeSplited[1][:5] 
                    count =0 
                addr=data_decoded['x']['out'][0]['addr'] 
            print(dataList) 
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {0}/{1}'
                  .format(msg.topic(), msg.partition()))
        else:
            print('Error occured: {0}'.format(msg.error().str()))

except KeyboardInterrupt:
    pass

finally:
    c.close()