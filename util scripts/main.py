import boto3
import requests
import yelpapi
import tqdm
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import requests




def get_restaurant():
    yelp_api = yelpapi.YelpAPI(
        "uCyK9WJjHFYT5Sx7DFdT9ERqTbOZcy8nU6sc_LkqAqfk5myYDJbQT2Kha7FxYeO8eR7UHytXjY7hgn5xDBF_JbtkNNcwaKFf0osgbP8SiWwrQ6zIMClUx0ynmGSDX3Yx")
    list_to_search = ["Indian","Italian","Mexican","Chinese","Thai","Spanish","Japanese","Korean","American"]
    # list_to_search = ["Indian"]
    key_wanted = ["id", "name", "review_count", "coordinates", "display_phone", "location", "rating"]
    data = {key: [] for key in list_to_search}
    for each in list_to_search:
        for i in tqdm.tqdm(range(0, int(1000 / 50 - 1))):
        # for i in tqdm.tqdm(range(0, 2)):
            search_results = yelp_api.search_query(location="Manhattan", term=each, limit=50, offset=i * 50)
            temp = []
            for items in search_results["businesses"]:
                temp_dict = {key: items[key] for key in key_wanted}
                temp_dict["zip_code"] = temp_dict["location"]["zip_code"]
                temp_dict["location"] = temp_dict["location"]["display_address"]
                temp_dict["cuisine"] = each
                for key in temp_dict.keys():
                    temp_dict[key] = {"S": str(temp_dict[key])}
                # temp_dict = {
                #     'PutRequest': {
                #         'Item': temp_dict
                #     }
                # }
                # print(temp_dict)
                data[each].append(temp_dict)
            time.sleep(0.2)
    return data

if __name__ == '__main__':

    data = get_restaurant()

    client = boto3.client('dynamodb',region_name='us-east-1')
    count = 0

    for key in data.keys():
        each = data[key]
        print(len(each))
        for i in tqdm.tqdm(range(0,len(each))):
            each[i]["insertedAtTimestamp"] = {"S": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
            # print(each[0][i])
            response = client.put_item(
                TableName = "Restaurant",
                Item = each[i]
            )
            count +=1

    print(count)

    host = 'search-chatbotsearch2-4ywqhfyrczguas2n5yis3kb2bq.us-east-1.es.amazonaws.com'  # For example, my-test-domain.us-east-1.es.amazonaws.com

    region = 'us-east-1'  # e.g. us-west-1

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
    for key in data.keys():
        each = data[key]
        for i in tqdm.tqdm(range(0, len(each))):

            document = {
                "cuisine": str(key)
            }

            es.index(index="restaurants", doc_type="Restaurant", id=each[i]["id"]["S"], body=document)



