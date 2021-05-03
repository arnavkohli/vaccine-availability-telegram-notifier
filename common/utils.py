import requests

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

def get_calendar_by_pin(pincode: int, date: str) -> dict:
	url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
	print ("url", url)
	headers = {
		"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
		"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"accept-encoding" : "gzip, deflate, br",
		"accept-language" : "en-US,en;q=0.9"
	}
	request = requests.get(url, headers=headers)
	print ("api setu response", request.content)
	if request.status_code == 200:
		data = request.json()
		data['success'] = True
		return data
	return {"success" : False}

def generate_message(data: dict):
	message = ""
	centers = data.get("centers")
	for center in centers:
		available = False
		message += f"Pincode: {center.get('pincode')}\n"
		message += f"Centre Name: {center.get('name')}\n"
		message += f"From: {center.get('from')}\n"
		message += f"To: {center.get('to')}\n\n"

		for index, session in enumerate(center.get('sessions', [])):
			if session.get('available_capacity') == 0:
				continue
			available = True
			if index == 0:
				message += f"Sessions/ Slots: \n"
			message += f"Min Age Limit: {session.get('min_age_limit')}\n"
			message += f"Available Capacity: {session.get('available_capacity')}\n"
			message += f"Vaccine: {session.get('vaccine')}\n"
			message += f"Slots Available In: {', '.join(session.get('slots'))}\n"

		if not available:
			message += f"No slots found for {center.get('pincode')}!\n"
	return message.strip()
