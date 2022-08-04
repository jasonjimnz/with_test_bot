# Python Telegram Did Rocket Launched Bot? MiniGame

A Python based project for a Telegram bot that
plays with you an image selection based minigame

# Requirements
- Python 3.8+
- asyncio
- python-telegram-bot --pre (The v20.x version)
- A bot registered in Telegram's Bot Father for 
  getting the bot token, is required to connect
  with Telegram's bot system


## Installation
Clone this repo in your environment, I suggest
you to have a virtual environment or anaconda 
installed, install the requirements, copy the 
config.json.bak file to config.json with your
Telegram's bot token, also you can avoid this
setting a TELEGRAM_BOT_TOKEN environmental
variable in your system, once all the requirements
are satisfied run the [main.py](main.py) file

```shell
pip install -r requirements.txt
python main.py
```

## Running on Docker
A [Dockerfile](Dockerfile) is provided in this repo
if you clone the repo and want to run the service
with Docker, follow these instructions, the token is
suggested to be as environmental variable but you
can use config.json file if you want to

```shell
docker build -t telegram_bot .
docker run -d --env TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN" telegram_bot
```
