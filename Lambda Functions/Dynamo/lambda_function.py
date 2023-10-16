import json
import boto3

from datetime import datetime
from decimal import Decimal


def lambda_handler(event, context):
    
    print("Uploading Restaurant data to DynamoDB...")
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("Dinningdb")
    
    with open("yelp_restaurants_data.json") as json_file:
        json_data = json_file.read()
        
    restaurants = json.loads(json_data)
    
    for restaurant in restaurants:
        
        item = {
            'id': restaurant['id'],
            'name': restaurant['name'],
            'address': restaurant['location']['address1'],
            'coordinates': {
                'latitude': Decimal(str(restaurant['coordinates']['latitude'])),
                'longitude': Decimal(str(restaurant['coordinates']['longitude']))
            },
            'num_reviews': restaurant['review_count'],
            'rating': Decimal(str(restaurant['rating'])),
            'zip_code': restaurant['location']['zip_code'],
            'insertedAtTimestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        table.put_item(Item=item)
            
    return {
        'statusCode': 200,
        'body': json.dumps('Restaurant data uploaded successfully!')
    }
