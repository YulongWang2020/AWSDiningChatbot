import json
# from requests_aws4auth import AWS4Auth
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import requests

def poll_sqs():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/043550019784/ChatbotSQS'
    sqs = boto3.client("sqs")
    sqsresponse = sqs.receive_message(QueueUrl=queue_url)
    
    message = sqsresponse['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    return sqsresponse
    
    
def lambda_handler(event, context):
    # print(poll_sqs())

    
    try:
        sqsresponse = poll_sqs()
    except:
        print("no message")
        return {}
    # print(sqsresponse["Messages"][0]["Body"])
    sqsresponse = sqsresponse["Messages"][0]["Body"]
    sqsresponse = sqsresponse.replace("\'", "\"")
    sqsresponse = json.loads(sqsresponse)
    print(sqsresponse)
    cuisine = sqsresponse["cuisine"]
    print(cuisine)
    host = 'search-chatbotsearch2-4ywqhfyrczguas2n5yis3kb2bq.us-east-1.es.amazonaws.com'
    url = "https://search-chatbotsearch-x3n3loze2vb7dphqgp2ldgstue.us-east-1.es.amazonaws.com"
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    result = es.search(
    index="restaurants",
    body={
        "query": {
            "match":{
                "cuisine": cuisine
                }
            }
        }
    )
    print(result)
    dynamodb = boto3.client('dynamodb')
    sns_messages = ""
    i = 0
    for each in result["hits"]["hits"]:
        print(each["_id"])
        dyresponse = dynamodb.get_item(
        TableName='Restaurant',
        Key={
            'id': {"S": each["_id"]}
            }
        )
        dyresponse = dyresponse["Item"]
        sns_messages += str(i+1) +": " +"\n" + "Name: "+ dyresponse["name"]["S"] +"\n" + "Location: " + dyresponse["location"]["S"].replace("\'", "").replace("\"", "").replace("[", "").replace("]","") + "\n" + "Rating: "  +dyresponse["rating"]["S"] + "\n"  +"Number: " + dyresponse["display_phone"]["S"] + "\n"
        print(dyresponse)
        i +=1
    
    sns = boto3.client("sns")
    sns.publish(
    PhoneNumber="+1"+sqsresponse["phonenumber"],
    Message=sns_messages)
    return {}
