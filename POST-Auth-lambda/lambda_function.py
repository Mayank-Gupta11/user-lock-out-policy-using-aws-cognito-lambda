import json
import boto3
import json

pool_id = "#poolid"

client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    # TODO implement
    
    print(event)
    dict_of_event=event
    print(dict_of_event'userName'])
    my_user_name=dict_of_event'userName']
    
    update_response = client.admin_update_user_attributes(
    UserPoolId=pool_id,
    Username=my_user_name,
    UserAttributes=[
        {
            'Name': 'custom:static_time_of_user',
            'Value': '0'
        },
        {
            'Name': 'custom:count_limit_of_user',
            'Value': '0'
        }
    ]
    )
    
    return event