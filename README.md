# AWS Serverless Customer Data Pipeline

**Amazon S3 → AWS Lambda (Python) → Amazon DynamoDB**

## Overview
An event-driven serverless application that processes customer records from JSON files uploaded to Amazon S3 and stores them in a DynamoDB table. The project was implemented and tested in AWS `us-east-1` (N. Virginia).

**Verified outcome:** Uploading `customers-test.json` led to **3 customer records** appearing in the DynamoDB `Customers` table (October 23, 2026). CloudWatch log details have not yet been independently verified.

## Architecture

```text
customers-test.json
       |
       v
Amazon S3 bucket
(serverless-customer-data-235494792645)
       |  ObjectCreated event, suffix .json
       v
AWS Lambda: S3ToDynamoDB (Python 3.13)
       |  boto3: get_object / put_item
       v
Amazon DynamoDB: Customers
       |
       +--> 3 customer records confirmed

Lambda -> Amazon CloudWatch Logs (execution logging)
```

## AWS resources

| Component | Configuration |
|---|---|
| Region | `us-east-1` |
| S3 bucket | `serverless-customer-data-235494792645` |
| S3 event | `s3:ObjectCreated:*`, suffix `.json` |
| Lambda function | `S3ToDynamoDB` |
| Runtime | Python 3.13 |
| IAM execution role | `S3LambdaDynamoDBRole` |
| Inline IAM policy | `S3LambdaDynamoDBAccess` |
| DynamoDB table | `Customers` |
| Partition key | `customer_id` (String) |

## Workflow
1. Upload a `.json` object into the S3 bucket.
2. S3 sends an object-created event to the Lambda function.
3. Lambda reads the object with `boto3` and parses the JSON.
4. Lambda writes each customer item to DynamoDB using `put_item`.
5. Verify items using DynamoDB **Explore items → Scan → Run**.

## Lambda source code

Save the following as `lambda_function.py`:

```python
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
```

## Example input

Save as `customers-test.json` (the S3 trigger matches the `.json` suffix):

```json
[
  {"customer_id":"101","first_name":"John","last_name":"Smith","email":"john@example.com","city":"Boston","state":"MA"},
  {"customer_id":"102","first_name":"Mary","last_name":"Jones","email":"mary@example.com","city":"Chicago","state":"IL"},
  {"customer_id":"103","first_name":"Robert","last_name":"Brown","email":"robert@example.com","city":"Atlanta","state":"GA"}
]
```

## Deployment outline
1. Create an S3 bucket and keep **Block Public Access** enabled.
2. Create DynamoDB table `Customers` with String partition key `customer_id`.
3. Create IAM role `S3LambdaDynamoDBRole`, trusted by Lambda. Attach `AWSLambdaBasicExecutionRole` and a least-privilege inline policy permitting `s3:GetObject` for `arn:aws:s3:::serverless-customer-data-235494792645/*` and `dynamodb:PutItem` for `arn:aws:dynamodb:us-east-1:<ACCOUNT_ID>:table/Customers`. The working role also had `dynamodb:BatchWriteItem`, though the code uses `PutItem`.
4. Create event Lambda function `S3ToDynamoDB` with Python 3.13, selecting the existing IAM role.
5. Paste the Python code into `lambda_function.py` and deploy.
6. Add an S3 trigger: bucket above, all object-create events, suffix `.json`.
7. Upload the test JSON and inspect DynamoDB `Customers` items.

## Test evidence and troubleshooting

- **Initial observation:** The `Customers` table scan returned **0 items** after the first upload.
- **Diagnostic steps:** Confirmed the Lambda function overview included S3; inspected the trigger configuration and verified the correct bucket, `s3:ObjectCreated:*`, and `.json` suffix. The Monitor dashboard showed no recent invocations for the viewed period, which was not definitive proof of no invocation.
- **Resolution/test:** Uploaded a fresh file named `customers-test.json`, causing a new object-created event.
- **Result:** DynamoDB `Customers` subsequently displayed **3 records**. This confirms the pipeline worked for the successful test.
- **Outstanding verification:** Review `/aws/lambda/S3ToDynamoDB` log streams to capture the exact invocation and log messages.

## Operational notes
- DynamoDB table names are case-sensitive (`Customers` is not `customers`).
- IAM S3 resource must match the actual bucket exactly.
- S3 trigger suffix should be `.json`, including the dot.
- Uploading the same customer IDs again will overwrite matching DynamoDB items when using `put_item`.
- This is a demonstration pipeline: add schema validation, partial-failure handling, idempotency safeguards, monitoring, and dead-letter handling for production use.
- Remove unneeded AWS resources after testing to avoid charges.

## Skills demonstrated
AWS Lambda, Amazon S3 event notifications, DynamoDB, IAM least-privilege permissions, Python 3, boto3, JSON processing, event-driven architecture, AWS Console configuration, and troubleshooting.

## Suggested repository layout

```text
aws-s3-lambda-dynamodb/
├── README.md
├── lambda_function.py
└── sample-data/
    └── customers-test.json
```

**Security:** Do not commit AWS credentials, access keys, or customer-sensitive data. The sample names/emails are fictitious.
