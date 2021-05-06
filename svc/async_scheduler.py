import json
import aiohttp
import asyncio

import time
from .db import DB
from datetime import datetime
from common.utils import TelegramBot, get_calendar_by_pin, async_get_calendar_by_pin, generate_message, is_valid_indian_pincode

def timeit(func):
	async def wrapper(*args, **kwargs):
		startTime = time.time()
		await func(*args, **kwargs)
		print (f"--- Finished in {time.time() - startTime} seconds ---")
	return wrapper

async def process_batch(db, users_collection, session, date, group):
	pincode = group.get('pincode')
	try:
		chat_ids = [db.search(collection=users_collection, filters={"_id" : user_id}).get('chat_id') for user_id in group.get('user_ids')]
	except :
		print (f"[Scheduler] No user_ids found for pincode {pincode}. Skipping...")
		return []

	response, data = await async_get_calendar_by_pin(session, pincode, date)
	if response == 200:
		print (f"[Scheduler] SLOTS FOUND for {pincode}. Checking availability...")
		message = generate_message(data)
		message_type = "SLOTS_FOUND_REGARDLESS_OF_AVAILABILITY"
	else:
		print (f"[Scheduler] (response: {response}) No slots found for {pincode}")
		message = f"No slots found for {pincode}!"
		message_type = "NO_SLOTS_AVAILABLE"

	# Failsafe
	if not message or message.strip() == "":
		message = f"No slots found for {pincode}!"
		message_type = "NO_SLOTS_AVAILABLE"

	return [{"chat_id" : chat_id, "message" : message, "message_type" : message_type} for chat_id in chat_ids]

def flatten(*args):
	final = []
	for arg in args:
	     final += arg
	return final

@timeit
async def run(telegram_bot_key: str, mongo_conn_url: str, database: str, users_collection: str, groups_collection: str):
	'''
		Retrieves chat_ids of users from the same pincode group and notfies them
		if slots are available at that pincode.
	'''
	db = DB(mongo_conn_url).connect(database)

	tb = TelegramBot(telegram_bot_key)
	today = datetime.strftime(datetime.now(), "%d-%m-%Y")

	groups = db.search(collection=groups_collection, all=True)
	valid_groups = [group for group in groups if is_valid_indian_pincode(group.get('pincode'))]
	
	today = datetime.strftime(datetime.now(), "%d-%m-%Y")
	async with aiohttp.ClientSession() as session:
		tasks = []
		for group in valid_groups:
			task = asyncio.ensure_future(process_batch(db, users_collection, session, today, group))
			tasks.append(task)
		message_tasks_data = await asyncio.gather(*tasks)
	print ("Message Tasks Data Len:", len(message_tasks_data))
	print (message_tasks_data)
	message_tasks_data = flatten(*message_tasks_data)
	print (message_tasks_data)
	# message_tasks_data = flatten(message_tasks_data)
	# message_tasks_data = message_tasks_data[1]
	async with aiohttp.ClientSession() as new_session:
		tasks = []
		for message_task_data in message_tasks_data:
			print ("here")
			task = asyncio.ensure_future(tb.async_send_message(session=new_session, text=message_task_data.get("message"), chat_id=message_task_data.get("chat_id"), message_type=message_task_data.get("message_type")))
			tasks.append(task)
		responses = await asyncio.gather(*tasks)
	
	return responses

	