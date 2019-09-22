# Bitcoin Data Streaming


This application reads the realtime data from the https://www.blockchain.com/api/api_websocket and stream the data to the local API server using Kafkha.The Server captures the data from the Kafkha and store it Redis DataStore.


### Prerequisites

Python3
confluent-kafka 1.1.0
Redis 3.3.8


## Getting Started

*) Clone the project into your local workspace.


*) Install Redis in your local Server and start at port no :6379.

*) Install kafkha in to your local server and create topic in the kafkha for streaming purpouse using command

    $ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic testTopic

*) Kafka uses ZooKeeper, so first, start a ZooKeeper server on your system. You can use the script available with Kafka to get start single-node ZooKeeper instance.

    $ cd /usr/local/kafka
    $ bin/zookeeper-server-start.sh config/zookeeper.properties

*) Start the Kafka server:

    $ bin/kafka-server-start.sh config/server.properties
    
*) Create a virtual environment for the application and install all the requirements using command.

    $ pip install -r requirements.txt 

*) Run the bitcoin_producer.py to start streaming using command.

    $ python bitcoin_producer.py

*) Run the bitcoin_consumer.py to recieve data and store it in redis DataStore.


    $ python bitcoin_producer.py

*) Start the API server using command

    $ python manage.py startserver

