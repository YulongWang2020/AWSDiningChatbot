import json
import boto3
def lambda_handler(event, context):
	client = boto3.client('lex-runtime')
	response = client.post_text(
	    botName='Chatbot',
	    botAlias='prod',
	    userId='123',
		sessionAttributes = {"string":""},
	    inputText=event['messages'][0]['unstructured']['text']
	);

	message = response['message']

	return {
	    'headers': {   'Access-Control-Allow-Origin': '*'}, 
	    'messages': [ {'type': "unstructured", 'unstructured': {'text': message}  } ]
	}
