from .db import DB
from datetime import datetime
from common.utils import TelegramBot, get_calendar_by_pin, generate_message


def run(telegram_bot_key, mongo_conn_url, database, users_collection, groups_collection):
	'''
		Retrieves chat_ids of users from the same pincode group and notfies them
		if slots are available at that pincode.
	'''
	db = DB(mongo_conn_url).connect(database)

	tb = TelegramBot(telegram_bot_key)
	today = datetime.strftime(datetime.now(), "%d-%m-%Y")

	groups = db.search(collection=groups_collection, all=True)

	for group in groups:
		pincode = group.get('pincode')
		print (f"[Scheduler] Pincode: {pincode}")
		data = get_calendar_by_pin(pincode, today)
		chat_ids = [db.search(collection=users_collection, filters={"_id" : user_id}).get('chat_id') for user_id in group.get('user_ids')]
		print (f"[Scheduler] Data: {data}")
		if data.get("success", None) and data.get("centers", None) != None:
			print (f"[Scheduler] SLOTS FOUND for {pincode} !!!")
			message = generate_message(data)
			for chat_id in chat_ids:
				print (f"[Scheduler] --- Sending message to Chat ID: {chat_id}")
				tb.send_message(message, chat_id)
		else:
			print (f"[Scheduler] No slots found for {pincode}")
			for chat_id in chat_ids:
				print (f"[Scheduler] --- Sending message to Chat ID: {chat_id}")
				tb.send_message(message, chat_id)
