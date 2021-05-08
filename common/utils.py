import requests
import re
import aiohttp
import asyncio

class TelegramBot:

	def __init__(self, key: str):
		self.base = "https://api.telegram.org/bot{}/{}"
		self.key = key

	def send_message(self, text: str, chat_id: int) -> bool:
		url = self.base.format(self.key, "sendMessage")
		data = {
			"chat_id" : chat_id,
			"text" : text
		}
		request = requests.post(url, data=data)
		if request.status_code == 200:
			return True
		return False

	async def async_send_message(self, session, text, chat_id, message_type):
		url = self.base.format(self.key, "sendMessage")
		data = {
			"chat_id" : chat_id,
			"text" : text
		}
		async with session.post(url, data=data) as response:
			response = await response.json()
			print (f"[TelegramBot] Sent to {chat_id} ({message_type})")
			return response



def get_calendar_by_pin(pincode: int, date: str) -> dict:
	url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
	headers = {
		"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
		"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"accept-encoding" : "gzip, deflate, br",
		"accept-language" : "en-US,en;q=0.9"
	}
	request = requests.get(url, headers=headers)
	if request.status_code == 200:
		data = request.json()
		data['success'] = True
		return data
	return {"success" : False}

async def async_get_calendar_by_pin(session: aiohttp.ClientSession, pincode: str, date: str) -> (int, dict):
	url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
	headers = {
		"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
		"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"accept-encoding" : "gzip, deflate, br",
		"accept-language" : "en-US,en;q=0.9"
	}
	async with session.get(url, headers=headers) as response:
		try:
			result_data = await response.json()
			result_data["pincode"] = pincode
			await asyncio.sleep(1)
			return 200, result_data
		except:
			return 403, {"pincode" : pincode}


def generate_message(data: dict):
	message = ""
	x_line = "x" + "-"*38 + "x"
	message += f"{x_line}\nPincode: {data.get('pincode')}\n\n"

	centers = data.get("centers", [])

	status = "unavailable"

	if centers != []:
		for c_index, center in enumerate(centers):
			message += f"* Centre Name: {center.get('name')}\n"
			available = False
			for index, session in enumerate(center.get('sessions', [])):
				if session.get('available_capacity') == 0:
					continue

				available = True
				status = "available"

				if index == 0:
					message += f"Sessions/ Slots:\n"
				message += f" -> Min Age Limit: {session.get('min_age_limit')} yrs\n"
				message += f" -> Available Capacity: {session.get('available_capacity')}\n"
				message += f" -> Vaccine: {session.get('vaccine')}\n"
				message += f" -> Slots Available In: {', '.join(session.get('slots'))}\n\n"

			if not available:
				message += f" -> No available slots found!\n\n"
	else:
		message += f" -> No centers found!\n\n"

	message = message.strip()
	message += f"\n{x_line}"

	return message, status

def is_valid_indian_pincode(pincode):
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
    pattern = re.compile(regex)
    matches = re.match(pattern, pincode)
    return False if matches == None else True
