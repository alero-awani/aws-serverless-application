import json

# import requests
import json
import uuid
import os
import boto3
from datetime import datetime

# Prepare DynamoDB Client
USERS_TABLE = os.getenv("USERS_TABLE", None)
dynamodb = boto3.resource("dynamodb")
ddbTable = dynamodb.Table(USERS_TABLE)


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    route_key = f"{event['httpMethod']} {event['resource']}"

    # Set default response, override with data from DyanomoDB is any
    response_body = {"message": "Unsupported route"}
    status_code = 400
    headers = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

    try:
        # Get a list of all users
        if route_key == "GET /users":
            ddb_response = ddbTable.scan(AttributesToGet="ALL_ATTRIBUTES")
            response_body = ddb_response["Items"]
            status_code = 200

        # CRUD operations for a single User

        # Read a user by ID
        if route_key == "Get /users/{userid}":
            # get data from the database
            ddb_response = ddbTable.get_item(
                Key={"userid": event["pathParameters"]["userid"]}
            )
            # return single item instead of full DynamoDB response
            if "Item" in ddb_response:
                response_body = ddb_response["Item"]
            else:
                response_body = {}
            status_code = 200

        # Delete a user by ID
        if route_key == "DELETE /users/{userid}":
            # delete item in the database
            ddbTable.delete_item(Key={"userid": event["pathParameters"]["userid"]})
            response_body = {}
            status_code = 200

        # Create a new user
        if route_key == "POST /users":
            request_json = json.loads(event["body"])
            request_json["timestamp"] = datetime.now().isoformat()
            # generate unique id if it isn't present in the request
            if "userid" not in request_json:
                request_json["userid"] = str(uuid.uuid1())
            # update the database
            ddbTable.put_item(Item=request_json)
            response_body = request_json
            status_code = 200
            # Update a specific user by ID
        if route_key == "PUT /users/{userid}":
            # update item in the database
            request_json = json.loads(event["body"])
            request_json["timestamp"] = datetime.now().isoformat()
            request_json["userid"] = event["pathParameters"]["userid"]
            # update the database
            ddbTable.put_item(Item=request_json)
            response_body = request_json
            status_code = 200
    except Exception as err:
        status_code = 400
        response_body = {"Error:": str(err)}
        print(str(err))
    return {
        "statusCode": status_code,
        "body": json.dumps(response_body),
        "headers": headers,
    }
