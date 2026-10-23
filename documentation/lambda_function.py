import json
import boto3
from decimal import Decimal
from urllib.parse import unquote_plus

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Customers")

def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        print(f"Reading file: {key}")
        response = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(
            response["Body"].read().decode("utf-8"),
            parse_float=Decimal
        )
        customers = data if isinstance(data, list) else [data]
        for customer in customers:
            table.put_item(Item=customer)
            print(f"Inserted customer: {customer['customer_id']}")
    return {
        "statusCode": 200,
        "body": "Customer records inserted successfully"
    }
