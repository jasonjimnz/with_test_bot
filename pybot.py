import json
import logging
import os
import random
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from VideoUtils import VideoUtils
from WithRocketBot import RocketBot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bot_token = os.getenv('TELEGRAM_BOT_TOKEN', None)
if not bot_token:
    try:
        bot_token = json.load(open('./config.json', encoding='utf-8'))['bot_token']
    except FileNotFoundError:
        raise Exception("Not TELEGRAM_BOT_TOKEN environment variable defined or not existing config.json file")
    except KeyError:
        raise Exception("Not bot_token key present in config.json file")


def bisect(n, mapper, tester):
    """
    Runs a bisection.

    - `n` is the number of elements to be bisected
    - `mapper` is a callable that will transform an integer from "0" to "n"
      into a value that can be tested
    - `tester` returns true if the value is within the "right" range
    """

    if n < 1:
        raise ValueError("Cannot bissect an empty array")

    left = 0
    right = n - 1

    while left + 1 < right:
        mid = int((left + right) / 2)

        val = mapper(mid)

        if tester(val):
            right = mid
        else:
            left = mid

    return mapper(right)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello Let's play a Rocket Launch Game, type /check to get an image"
    )


async def get_frame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_file = VideoUtils.get_video()
    frame = random.randint(1, video_file.frames + 1)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=VideoUtils.video_frame_url(frame)
    )

# TODO: Add BotServer instance for getting game status
# TODO: After getting a frame, update game status
# TODO: After showing a frame, every answer should be caught
# TODO: Add a reminder handler if the user deletes the chat
# TODO: Add a reset handler
# TODO: Game status should check user game for reducing frame list based on iterations
# TODO: Modify bisect function, the logic should wait to user async interaction


def start_bot():
    pybot = RocketBot(bot_token)
    pybot.register_handler(CommandHandler('start', start))
    pybot.register_handler(CommandHandler('check', get_frame))
    pybot.run()
