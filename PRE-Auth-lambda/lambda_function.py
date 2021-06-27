import json
import boto3
import json
import time


pool_id = "#enter ur pool id here "

client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    
    dict_of_event=event
    print(dict_of_event['userName'])
    my_user_name=dict_of_event['userName']
    
    list_of_keys=list(dict_of_event['request']['userAttributes'].keys())
    print(list_of_keys)
    
    if 'custom:static_time_of_user' and 'custom:count_limit_of_user' not in list_of_keys:
        
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
            },
        ],
        )
        print(update_response)
        
        
        dict_of_event_updated=dict_of_event['request']['userAttributes']
        dict_of_event_updated.update({"custom:static_time_of_user":"0","custom:count_limit_of_user":"0"})
        
    
    
    updated_curr_count=dict_of_event['request']['userAttributes']['custom:count_limit_of_user']
    static_time_of_user=dict_of_event['request']['userAttributes']['custom:static_time_of_user']
    
    val=int(updated_curr_count)+1
    updated_curr_count=str(val)
    print(updated_curr_count)
    if int(updated_curr_count)>=5:
        if static_time_of_user=='0':
            future_user_time=time.time()+2*120
            static_time_of_user=str(future_user_time)
            
            update_response = client.admin_update_user_attributes(
            UserPoolId=pool_id,
            Username=my_user_name,
            UserAttributes=[
                {
                    'Name': 'custom:static_time_of_user',
                    'Value': static_time_of_user
                },
            ],
            )
            raise Exception("Password attempts exceeded. try after 4 minutes.")
            
        elif float(static_time_of_user)<time.time():
            # once 4 minutes are over.. intilize everything back to 0...
            
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
                },
            ],
            )
            
        else:
            raise Exception("Password attempts exceeded. Please try again in {} seconds. ".format(int(float(static_time_of_user)-time.time())))
        return event
    else:
        #update count..
        update_response = client.admin_update_user_attributes(
        UserPoolId=pool_id,
        Username=my_user_name,
        UserAttributes=[
            {
                'Name': 'custom:count_limit_of_user',
                'Value': updated_curr_count
            },
        ],
        )
        return event