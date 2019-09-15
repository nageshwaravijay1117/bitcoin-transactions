import json
from confluent_kafka import Producer
from websocket import create_connection
 
p = Producer({'bootstrap.servers': 'localhost:9092'})

ws = create_connection("wss://ws.blockchain.info/inv")
ws.send("""{"op":"unconfirmed_sub"}""")
currTime = ''
prev_time = '00:00'
count =0
dataList =[]
while True:
    tx = ws.recv()
    data_decoded=json.loads(tx) 
    hash=data_decoded['x'] 
    p.produce('mytopic', key='aa', value=tx)
    print("sent")
   