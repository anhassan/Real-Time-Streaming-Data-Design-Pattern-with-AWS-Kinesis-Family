import json
import base64
import uuid

def lambda_handler(event, context):
    output = []
    for record in event['records']:
        # Decoding the read records
        payload_json = json.loads(base64.b64decode(record['data']).decode('utf-8'))
        # Adding additional information to the records
        payload_json["number"] = str(uuid.uuid4())
        payload_updated = json.dumps(payload_json)
        
        # Forming the output record
        output_record = {
            'recordId' : record['recordId'],
            'result' : 'Ok',
            'data' : base64.b64encode(payload_updated.encode('utf-8')).decode('utf-8')
        }
        
        print("Record {}".format(record))
        
        # Creating the output batch to be sent
        output.append(output_record)
    
    # Logging the number of records transformed
    num_records_transformed = len(event['records'])
    print('Successfully transformed : {} number of records'.format(num_records_transformed))
    
    # Pushing out the transformed records
    return {'records' : output}
        
