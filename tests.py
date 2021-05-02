import os
import pytest
from datetime import datetime
from utils import TelegramBot, get_calendar_by_pin, generate_message

@pytest.fixture
def tester_chat_id():
	return os.getenv("TELEGRAM_CHAT_ID")

@pytest.fixture
def dummy_get_calendar_by_pin_response():
	return {
	  "centers": [
	    {
	      "center_id": 1234,
	      "name": "District General Hostpital",
	      "name_l": "",
	      "state_name": "Maharashtra",
	      "state_name_l": "",
	      "district_name": "Satara",
	      "district_name_l": "",
	      "block_name": "Jaoli",
	      "block_name_l": "",
	      "pincode": "413608",
	      "lat": 28.7,
	      "long": 77.1,
	      "from": "09:00:00",
	      "to": "18:00:00",
	      "fee_type": "Free",
	      "vaccine_fees": [
	        {
	          "vaccine": "COVISHIELD",
	          "fee": "250"
	        }
	      ],
	      "sessions": [
	        {
	          "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
	          "date": "31-05-2021",
	          "available_capacity": 50,
	          "min_age_limit": 18,
	          "vaccine": "COVISHIELD",
	          "slots": [
	            "FORENOON",
	            "AFTERNOON"
	          ]
	        }
	      ]
	    }
	  ]
	}

@pytest.fixture
def dummy_generate_message_response():
	return '''Pincode: 413608\nCentre Name: District General Hostpital\nFrom: 09:00:00\nTo: 18:00:00\n\nSessions/ Slots: \nAvailable Capacity: 50\nVaccine: COVISHIELD\nSlots Available In: FORENOON, AFTERNOON'''

def test_get_calendar_by_pin():
	data = get_calendar_by_pin(pincode=411021, date=datetime.strftime(datetime.now(), "%d-%m-%Y"))
	assert data.get("success") == True

def test_generate_message(dummy_get_calendar_by_pin_response):
	message = generate_message(dummy_get_calendar_by_pin_response)
	expected = '''Pincode: 413608\nCentre Name: District General Hostpital\nFrom: 09:00:00\nTo: 18:00:00\n\nSessions/ Slots: \nAvailable Capacity: 50\nVaccine: COVISHIELD\nSlots Available In: FORENOON, AFTERNOON'''
	assert message == expected

def test_telegram_bot(dummy_generate_message_response, tester_chat_id):
	tb = TelegramBot(os.getenv("TELEGRAM_BOT_KEY"))
	chat_id = tester_chat_id
	assert tb.send_message(dummy_generate_message_response, chat_id=chat_id) == True

