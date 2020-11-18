import json

def lambda_handler(event, context):
    
    response = {
       "sessionAttributes":{
           "currentReservation": "{\"ReservationType\":\"Hotel\",\"Location\":\"Moscow\",\"RoomType\":null,\"CheckInDate\":null,\"Nights\":null}"
       },
       "dialogAction":{
          "type":"Delegate",
          "slots":event["currentIntent"]["slots"]
       }
    }
    
    return response
