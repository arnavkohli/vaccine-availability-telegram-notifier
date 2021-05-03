import os
import argparse
from datetime import datetime
from common.utils import TelegramBot, get_calendar_by_pin, generate_message

def check_if_env_vars_loaded(names):
	return [name for name in names if not os.getenv(name)]

def run(pincodes):
	tb = TelegramBot(os.getenv("TELEGRAM_BOT_KEY"))
	chat_id = os.getenv("TELEGRAM_CHAT_ID")
	today = datetime.strftime(datetime.now(), "%d-%m-%Y")
	
	for pincode in pincodes:
		data = get_calendar_by_pin(pincode, today)
		if data.get("success", None) and data.get("centers", None) != None:
			message = generate_message(data)
			tb.send_message(message, chat_id)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--pincodes', type=int, nargs='+', help='List of Pincodes to check for.')
	args = parser.parse_args()
	if not args.pincodes:
		exit("[SCRIPT] Please enter atleast one pincode! Ex: python script.py --pincodes 411021")

	# Look for .env file
	if os.path.isfile(".env"):
		# Load using python-dotenv
		from dotenv import load_dotenv
		load_dotenv()
		not_loaded_vars = check_if_env_vars_loaded(['TELEGRAM_BOT_KEY', 'TELEGRAM_CHAT_ID'])
		if not_loaded_vars:
			exit(f"[SCRIPT] Following env var(s) not found in .env file: {', '.join(not_loaded_vars)}")
		run(args.pincodes)
	else:
		exit("[SCRIPT] Please input bot key using arg parser or .env file.")
