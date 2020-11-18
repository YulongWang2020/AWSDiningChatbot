I used two "LF1" lambda functions, LF1 is used to fulfill the intent that is called by lex at the end of session when fulfilled. 
LF1_1 is used for code hook and being called by Lex every time a message is sent.

In the main.py, I search using the yelp api and send them to Dynamodb first and then send to ES.