<h1 align="center"> Vaccine Availability Telegram Notifier </h1>

<p align="center">
  <img src="https://github.com/arnavkohli/vaccine-availability-telegram-notifier/actions/workflows/ci.yml/badge.svg" />
</p>

<p align="center">
    With the initiation of the COVID vaccination drive across India for all individuals above the age of 18, I wrote a simple vaccine notifier script which alerts the user regarding open slots in the vicinity, via Telegram.
 </p>


## Setup

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

### Run tests
```
pytest tests.py
```

<p align="center">
  <img src="https://github.com/arnavkohli/vaccine-availability-telegram-notifier/blob/master/screenshot.png" /><br>
  <em>Sample Notification</em>
</p>
