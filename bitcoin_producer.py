"""
==========================================
Author:Nageshwara Vijay
Created-At:15-09-2019
Last-Modified:17-09-2019
==========================================
"""
import json
from confluent_kafka import Producer
from websocket import create_connection

#Producer Object is Created
p = Producer({'bootstrap.servers': 'localhost:9092'})

#Connecting to Blockchain Stream and Pushing Data to Consumer Using Producer
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
   