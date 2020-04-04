# Coronavirus-World_Tracker

A Slackbot+Telegram bot that gives latest updates about confirmed COVID-19 cases all over world, pulling the information from the website (https://www.worldometers.info/coronavirus/) & (https://www.worldometers.info/coronavirus/#countries) with a csv file as attachment to view all the data of the countries.

![Coronavirus-World-Tracker](https://github.com/Kaustav96/Coronavirus-World_Tracker/blob/master/world1.PNG)
![Coronavirus-World-Tracker](https://github.com/Kaustav96/Coronavirus-World_Tracker/blob/master/world2.PNG)
![Coronavirus-World-Tracker](https://github.com/Kaustav96/Coronavirus-World_Tracker/blob/master/world3.PNG)

## Features
- Sit back and relax - the coronavirus updates will come to you.
- Get Slack notifications (picture below)
  -  New Corona Virus cases happening all over world
  -  How many people have Corona Virus per Country?
  -  How many deaths happened per Country?
  -  The new Countries entering the corona zone.
- Its reliable - the source of data is official website ([here](https://www.worldometers.info/coronavirus/)) & ([here](https://www.worldometers.info/coronavirus/#countries))
- Its ROBUST! 
  - What if script fails? What if the website changes format?
  - You get Slack notifications about the exceptions too.
  - You have log files (check `bot.log`) too, to evaluate what went wrong
  
 
 ## Installation
- You need Python
- You need a Slack account + Slack Webhook to send slack notifications to your account
- You need a new bot in telegram to send notifications cross telegram also.
- Use the instructions here to generate the bot token and get the group id: https://dev.to/mddanishyusuf/build-telegram-bot-to-send-daily-notification-4i00
- Install dependencies by running
```bash
pip install tabulate
pip install requests
pip install python-telegram-bot
pip install beautifulsoup4
pip install telegram
```
- Clone this repo and create auth.py
```bash
git clone https://github.com/Kaustav96/Coronavirus-World-Tracker.git
cd Coronavirus-World-Tracker
touch auth.py
```
- Write your Slack Webhook into auth.py
```python
DEFAULT_SLACK_WEBHOOK = 'https://hooks.slack.com/services/<your custome webhook url>'
```
