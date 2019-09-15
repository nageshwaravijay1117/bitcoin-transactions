import json
from websocket import create_connection
from datetime import datetime
import redis
from confluent_kafka import Producer
# if you encounter a "year is out of range" error the timestamp# may be in milliseconds, try `ts /= 1000` in that caseprint(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
# ws = create_connection("wss://ws.blockchain.info/inv")
# ws.send("""{"op":"unconfirmed_sub"}""")
# currTime = ''
# prev_time = '00:00'
# count =0
# dataList =[]
# while True:
#     tx = ws.recv()
#     data_decoded=json.loads(tx) 
#     hash=data_decoded['x'] 
#     tmpDate=data_decoded['x']['time'] 
#     timeOfTran=datetime.utcfromtimestamp(int(tmpDate)).strftime('%Y-%m-%d %H:%M:%S') 
#     timeSplited= timeOfTran.split() 
#     print('\n ',timeSplited[6:]) 
#     count+=1 
#     currTime = timeSplited[1][:5] 
#     if timeSplited[1][6:] == '00':
#         print('asd') 
#         if prev_time != currTime:
#             prev_time = currTime
#             dataList.append({currTime:count}) 
#             currTime = timeSplited[1][:5] 
#             count =0 
#         addr=data_decoded['x']['out'][0]['addr'] 
#     print(dataList) 

r = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

print(r.get('15:11'))
