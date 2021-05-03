import os
import json
import boto3
from svc.scheduler import run

def lambda_handler(event, context):
	try:
	    run(
	    	telegram_bot_key = os.getenv("TELEGRAM_BOT_KEY"),
			mongo_conn_url = os.getenv("MONGO_CONN_URL"),
			database = os.getenv("DATABASE"),
			users_collection = os.getenv("USER_COLLECTION"),
			groups_collection = os.getenv("GROUP_COLLECTION")
	    )
	    return {
	        'statusCode': 200,
	        'body': json.dumps('Daily word sent.')
	    }
	except Exception as err:
		return {
	        'statusCode': 404,
	        'body': json.dumps(f'There was an error: {err}')
	    }
	
if __name__ == "__main__":   
    lambda_handler('', '')
