import os
import json
import boto3
import random


def getData(iotName, lowVal, highVal):
    data = {}
    data['iotName'] = iotName
    data['iotValue'] = random.randint(lowVal, highVal)
    return data


while 1:
    kinesis = boto3.client('kinesis')
    rnd = random.random()
    if (rnd < 0.01):
        data = json.dumps(getData('DemoSensor', 100, 120))
        kinesis.put_record(
                StreamName=os.environ['STREAM_NAME'],
                Data=data,
                PartitionKey='shardId-000000000000')
        print('***************************** anomaly ************************* {}'.format(data))
    else:
        data = json.dumps(getData('DemoSensor', 10, 20))
        kinesis.put_record(
                StreamName=os.environ['STREAM_NAME'],
                Data=data,
                PartitionKey='shardId-000000000000')
        print(data)
