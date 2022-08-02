FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Run with ENV flag with the Telegram bot token
CMD [ "python3", "main.py" ]