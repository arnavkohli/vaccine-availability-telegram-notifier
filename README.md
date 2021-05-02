# Vaccine Availability Telegram Notifier
![workflow](https://github.com/arnavkohli/vaccine-availability-telegram-notifier/actions/workflows/ci.yml/badge.svg)

## Setup
```python
pip install -r requirements.txt
```

## Usage
```python
python script.py --pincodes 244413 627401
```

## Expected Environment Variables (inside *.env* file)

#### TELEGRAM_BOT_KEY
The Telegram BOT API key provided to you by BotFather.

#### TELEGRAM_CHAT_ID
The Telegram Chat ID of the chat the bot is a member of and also the one you want to be notified on.
