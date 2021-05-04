from .db import DB
from datetime import datetime
from common.utils import TelegramBot, get_calendar_by_pin, generate_message, is_valid_indian_pincode


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
		if not is_valid_indian_pincode(str(pincode)):
			print (f"[Scheduler] Invalid Pincode: {pincode}. Skipping...")
			continue

		print (f"[Scheduler] Pincode: {pincode}")
		data = get_calendar_by_pin(pincode, today)
		try:
			chat_ids = [db.search(collection=users_collection, filters={"_id" : user_id}).get('chat_id') for user_id in group.get('user_ids')]
		except:
			print (f"[Scheduler] No user_ids found for pincode {pincode}. Skipping...")
			continue
		print (f"[Scheduler] Data: {data}")


		if data.get("success", None) and data.get("centers", []) != []:
			print (f"[Scheduler] SLOTS FOUND for {pincode}. Checking availability...")
			message = generate_message(data)
			message_type = "SLOTS_FOUND_REGARDLESS_OF_AVAILABILITY"
		else:
			print (f"[Scheduler] No slots found for {pincode}")
			message = f"No slots found for {pincode}!"
			message_type = "NO_SLOTS_AVAILABLE"


		# Failsafe
		if not message or message.strip() == "":
			message = f"No slots found for {pincode}!"
			message_type = "NO_SLOTS_AVAILABLE"

		for chat_id in chat_ids:
			print (f"[Scheduler] ---> Sending message to Chat ID: {chat_id}; Message Type: {message_type}")
			tb.send_message(message, chat_id)
