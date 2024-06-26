import json

from opensearchpy import OpenSearch, RequestsHttpConnection

print("Uploading Restaurant data to OpenSearch started...")

opensearch = OpenSearch(
    hosts = ["Open Search End point Link"],
    http_auth = ('User Name', 'Password'),
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    connection_class = RequestsHttpConnection
)

mapping = {
    "mappings": {
        "properties": {
            "id": {
                "type": "text"
            },
            "cuisine": {
                "type": "text"
            }
        }
    }
}

opensearch.indices.create(index='restaurants', body=mapping)

with open("yelp_restaurants_data.json") as json_file:
    json_data = json_file.read()
    
restaurants = json.loads(json_data)

for restaurant in restaurants:    
    document = {
        "id": restaurant['id'],
        "cuisine": restaurant.get('cuisine', 'unknown')
    }
    opensearch.index(index="restaurants", body=document)

print("Uploading Restaurant data to OpenSearch completed!")
