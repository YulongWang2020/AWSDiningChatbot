import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    lexmessage = event["currentIntent"]["slots"]["Cuisine"]+","+event["currentIntent"]["slots"]["location"]+","+event["currentIntent"]["slots"]["Phonenumber"]
    client = boto3.client('sqs')
    response = client.send_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/043550019784/ChatbotSQS',
    MessageBody=str({
        "cuisine": str(event["currentIntent"]["slots"]["Cuisine"]),
        "phonenumber":str(event["currentIntent"]["slots"]["Phonenumber"])
        })
    )
    print(str({
        "cuisine":event["currentIntent"]["slots"]["Cuisine"],
        "phonenumber":event["currentIntent"]["slots"]["Phonenumber"]
        }))
    
    return {
     "sessionAttributes": {},
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Thanks, we have received your request and will SNS the list of restaurant soon!"
            }
        }
    }
