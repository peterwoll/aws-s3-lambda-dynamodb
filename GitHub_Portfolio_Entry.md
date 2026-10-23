# GitHub Portfolio Entry - AWS Serverless Customer Data Pipeline

## Project title
AWS Serverless Customer Data Pipeline | S3, Lambda, Python & DynamoDB

## Short description
Built and tested an event-driven AWS application that automatically reads customer JSON files from Amazon S3, processes them with a Python Lambda function, and inserts records into Amazon DynamoDB.

## Portfolio description
Designed and implemented a serverless customer data ingestion pipeline in AWS us-east-1. Configured S3 ObjectCreated notifications to invoke a Python 3.13 Lambda function, used boto3 to retrieve and parse JSON objects, and stored customer records in a DynamoDB table with a String partition key. Set up an IAM execution role with scoped S3 read and DynamoDB write permissions. Troubleshot an initially empty table by reviewing the event trigger configuration and retesting with a new S3 upload. Verified successful end-to-end processing when three customer records appeared in DynamoDB.

**Technology:** AWS S3 · AWS Lambda · Amazon DynamoDB · IAM · CloudWatch (logging configured; logs not yet verified) · Python 3.13 · boto3 · JSON

**Outcome:** 3 customer records successfully inserted and verified in DynamoDB on October 23, 2026.

## Suggested GitHub repository
`aws-s3-lambda-dynamodb`

## Suggested LinkedIn project description
Implemented a Python-based AWS serverless pipeline using Amazon S3 event notifications, AWS Lambda, and DynamoDB. Configured IAM access, developed JSON ingestion logic with boto3, troubleshot event processing, and verified successful insertion of three customer records. Documented architecture, deployment steps, and testing for reproducibility.

## Suggested topics
`aws` `serverless` `lambda` `s3` `dynamodb` `python` `boto3` `event-driven-architecture`

## Before publishing
Upload README.md and lambda_function.py; optionally include the fictitious sample JSON. Do not upload secrets, credentials, private customer data, or AWS access keys. Add a sanitized screenshot of DynamoDB results if desired.
