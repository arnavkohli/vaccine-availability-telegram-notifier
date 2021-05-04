<h1 align="center"> Vaccine Availability Telegram Notifier </h1>

<p align="center">
  <img src="https://github.com/arnavkohli/vaccine-availability-telegram-notifier/actions/workflows/ci.yml/badge.svg" />
  <img src="https://visitor-badge.laobi.icu/badge?page_id=vaccine-availability-telegram-notifier" />
</p>

<p align="center">
    With the initiation of the COVID vaccination drive across India for all individuals above the age of 18, I wrote a telegram bot which alerts the user regarding open slots in the vicinity!
 </p>
 
 <p align="center">
    <a href="https://t.me/KohlGuysBot">Check it out!</a>
 </p>

## Project Overview

- *svc* - Registration API
- *telegram_bot* - Telegram Bot code.
- *lambda_function.py* - Scheduler code for the AWS Lambda function.
- *script.py* - Script to run the notifier once.

## Script Setup

You can also run the local script with your own configurations.

### Clone this Repository
```
git clone https://github.com/arnavkohli/vaccine-availability-telegram-notifier.git
```

### Navigate to the cloned directory & install the dependencies
```
pip install -r requirements.txt
```

### Update environment variables
Open the file *.env* and replace the dummy values with a legitimate Telegram Bot Key and a Telegram Chat ID.
```
TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY_HERE>
TELEGRAM_CHAT_ID=<TELEGRAM_CHAT_ID_HERE>
```

### Run the script
```
python script.py --pincodes 244413 627401
```

## Testing

### Set environment variables
Following variables are expected to be set in the environment before running the tests.

```
TELEGRAM_BOT_KEY
TELEGRAM_CHAT_ID
```
