# Task
X Profile Monitoring with Telegram Alerts
```
 Build a custom bot that monitors specific profiles on X (formerly Twitter) for posts indicating a **tax** **break** etc. The bot should notify **via Telegram** as soon as one of the monitored accounts posts a relevant update.
```

# Overview

## Install
```
# from python virtual env
cd proposals\web_scraping_xplatform_alert_telegram
pip install -r requirements.txt
```

## Run
List of files:
- bot_lookup_words.csv contains list of words X platform will be serched for
- public_profiles.csv list of x (twitter) profiles
- bot_alert.py telegram message pusher
```
# run script to get instructions for telegram
python bot_alert.py
```
- For now set the telegram token in the bot.py class Bot.__init__ method
- Run bot.py
```
python bot.py
```

Note: if you haven't set the telegram token, then in logs you'll have 'SOURCE:' messages with looked up data