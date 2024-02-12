from faker import Faker
import json
import boto3


# Utility function to generate a batch of defined number of records
def generate_batch(batch_size,fake):
    records = []
    for index in range(batch_size):
        records += [{
                "name":    fake.name(),
                "url":     fake.url(),
                "email":   fake.email(),
                "country": fake.country()
            }]
    
    batch = [ {
                'Data' : json.dumps(record),
                'PartitionKey' : str(hash(record['name']))
             }
        for record in records
        ]
    
    return batch


# Utility function to send a batch of records to a defined Kinesis Data Stream
def send_batch_to_kinesis_data_stream(batch,client,stream_name):
    response = client.put_records(
        Records = batch,
        StreamName = stream_name
        )
    return response
        

if __name__ == '__main__':
    
    # Deciding the number of records to be sent as a batch
    BATCH_SIZE = 100
    # Deciding the number of batches to be sent
    NUM_BATCHS = 5
    # Name of the destination Kinesis Data Stream
    KINESIS_STREAM = 'kinesis-data-stream'
    # Creating kinesis client
    kinesis_client = boto3.client('kinesis')
    
    fake = Faker()
    
    # Dispatching batchs of records to defined Kinesis Data Stream
    for batch_num in range(0,NUM_BATCHS):
        batch = generate_batch(BATCH_SIZE,fake)
        response = send_batch_to_kinesis_data_stream(batch,kinesis_client,KINESIS_STREAM)
        print("Loaded Batch Number : {} with Response : {}".format(batch_num,str(response)) )








