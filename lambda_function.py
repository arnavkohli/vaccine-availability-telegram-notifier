import os
import json
import boto3
import asyncio
from svc.async_scheduler import run

def lambda_handler(event, context):
	try:
	    asyncio.run(run(
	    	telegram_bot_key = os.getenv("TELEGRAM_BOT_KEY"),
			mongo_conn_url = os.getenv("MONGO_CONN_URL"),
			database = os.getenv("DATABASE"),
			users_collection = os.getenv("USER_COLLECTION"),
			groups_collection = os.getenv("GROUP_COLLECTION"),
			vip=False,
			notify_on_unavailability=True
	    ))
	    return {
	        'statusCode': 200,
	        'body': json.dumps('Run successful')
	    }
	except Exception as err:
		return {
	        'statusCode': 404,
	        'body': json.dumps(f'There was an error: {err}')
	    }
	
if __name__ == "__main__":   
    lambda_handler('', '')
