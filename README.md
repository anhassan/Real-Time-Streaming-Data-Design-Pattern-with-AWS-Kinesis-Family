# Introduction
The Amazon Kinesis family provides a suite of services for real-time streaming data processing. With Kinesis Data Streams, we can ingest and process large volumes of streaming data using custom applications. Kinesis Data Firehose simplifies loading streaming data into AWS data stores and analytics services without the need for coding. For real-time analysis, Kinesis Data Analytics allows us to process streaming data using SQL or Apache Flink without managing infrastructure. Additionally, Kinesis Video Streams enables secure streaming of video from connected devices for real-time processing and analysis. These services empower the development of scalable and responsive applications for various use cases including IoT, log analysis, monitoring, and more.

# Design and Implementation

We are going to implement a data pattern where a producer generates events in real-time. These events will be ingested by an ingestion hub capable of handling messages in real-time. Finally, we'll have a downstream component where these messages are pushed after undergoing transformation from their raw ingested state.

## *How is the data pattern implemented?*

1.  A Kinesis Data Stream is created which would be the hub for ingesting the messages produced by producer in real time
    
2.  A producer application is created in AWS Cloud9 which is responsible for sending anonymous user data messages (using faker api) to Kinesis Data Stream shard using the kinesis client

The producer application code is present in the repository with the name of `producer.py` for reference

3.  A Kinesis Data Firehose delivery stream is created which acts as a real time ETL (Extract Transform Load) solution as it does the following:
-   Extracts data from the Kinesis Data Stream shards
    
-   Performs transformation logic on the ingested Kinesis Data Stream records. In our case the transformation involves addition of an additional attribute in the sourced json using lambda functions
    
The code for the transformation logic is present in the repository with the name of `lambda_firehose_transformation.py` for reference

Here is the sample of the record received by lambda function:
```json
{  
"recordId":"49649158622693748790371174676937468892771630995526909954000000",  
"approximateArrivalTimestamp":1707628780995,  
"data":"eyJuYW1lIjogIkFtYW5kYSBGdWxsZXIiLCAidXJsIjogImh0dHBzOi8vaHVhbmctcm9zZS5pbmZvLyIsICJlbWFpbCI6ICJibGFrZTU3QGV4YW1wbGUuY29tIiwgImNvdW50cnkiOiAiQW5nb2xhIn0=",  
"kinesisRecordMetadata":{  
"sequenceNumber":"49649158622693748790371174676937468892771630995526909954",  
"subsequenceNumber":0,  
"partitionKey":"6675637409711158518",  
"shardId":"shardId-000000000000",  
"approximateArrivalTimestamp":1707628780995  
}  
}
```

-   Loads the data into the destination target which in our case is a S3 bucket

How often the data is loaded into the target destination depends upon the Buffer Size and Buffer Time. The batch is loaded in the target when either of the two is met (either Buffer Size or Buffer Time is exceeded)

The architectural design of the entire data pattern is added below for ease of understanding
