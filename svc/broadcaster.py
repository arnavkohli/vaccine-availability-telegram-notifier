from .db import DB
from datetime import datetime
from common.utils import TelegramBot

def broadcast_message(telegram_bot_key, mongo_conn_url, database, users_collection, message):
	'''
		Broadcasts message to all users.
	'''
	db = DB(mongo_conn_url).connect(database)

	tb = TelegramBot(telegram_bot_key)

	users = db.search(collection=users_collection, all=True)

	for user in users:
		tb.send_message(message, user.get("chat_id"))
		print (f"[Broadcaster] Sent message to username: {user.get('telegram_username')}; first_name: {user.get('first_name')}")
