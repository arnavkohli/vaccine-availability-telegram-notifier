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
		print (request.content)
		print (url)
		return False

def get_calendar_by_pin(pincode: int, date: str) -> dict:
	url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
	request = requests.get(url)

	if request.status_code == 200:
		data = request.json()
		data['success'] = True
		return data
	return {"success" : False}

def generate_message(data: dict):
	message = ""
	centers = data.get("centers")
	for center in centers:
		message += f"Pincode: {center.get('pincode')}\n"
		message += f"Centre Name: {center.get('name')}\n"
		message += f"From: {center.get('from')}\n"
		message += f"To: {center.get('to')}\n\n"

		for index, session in enumerate(center.get('sessions', [])):
			if index == 0:
				message += f"Sessions/ Slots: \n"
			message += f"Available Capacity: {session.get('available_capacity')}\n"
			message += f"Vaccine: {session.get('vaccine')}\n"
			message += f"Slots Available In: {', '.join(session.get('slots'))}\n"

	return message.strip()
