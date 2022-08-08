import json
import logging
import os
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot_game import BotHandler, game_validator
from video_utils import VideoUtils
from rocket_bot import RocketBot
from bisect_machine import StateBisect

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

game_handler = BotHandler()


def get_user_data(update: Update, new_one: bool = False):
    user_id = update.effective_user.id
    user_game = game_handler.get_user_game(str(user_id))
    if user_game['updated_at'] is None or new_one:
        video_file = VideoUtils.get_video()
        user_game_state = StateBisect(total_elements=video_file.frames)
        game_handler.set_user_game(
            user_id=str(update.effective_user.id),
            game_state=user_game_state.serialize_bisect_state()
        )
    else:
        user_game_state = StateBisect.get_bisection_from_state(user_game['state'])
    return user_id, user_game, user_game_state


async def send_game_message(update: Update,  context: ContextTypes.DEFAULT_TYPE, user_game_state):
    frame = user_game_state.get_mid_value()
    await context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=VideoUtils.video_frame_url(frame)
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Did rocket launch yet? answer in /rocket_launched ( /Yes or /No )"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello Let's play a Rocket Launch Game, type /get_image to "
             "get an image or /help for getting instructions"
    )


async def get_frame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id, user_game, user_game_state = get_user_data(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Getting images, this could take few seconds"
    )
    await send_game_message(update, context, user_game_state)


async def update_bisect(
        user_id: int,
        user_game_state: StateBisect,
        user_game: dict,
        bisect_status: bool,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    game_handler.set_user_game(
        user_id=str(user_id),
        game_state=user_game_state.serialize_bisect_state()
    )
    if bisect_status:
        await send_game_message(update, context, user_game_state)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"We found the frame {user_game_state.right} at"
                 f" {user_game['updated_at'].strftime('%a, %d %b %Y %H:%M:%S')}!"
        )


async def launch_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = "".join(context.args)
    user_id, user_game, user_game_state = get_user_data(update)

    if str(response).lower() in ['yes', 'y', 'true', 'no', 'n', 'false']:
        bisect_status = user_game_state.bisect_interaction(lambda n: game_validator(str(response)))
        await update_bisect(user_id, user_game_state, user_game, bisect_status, update, context)


async def launch_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id, user_game, user_game_state = get_user_data(update)
    bisect_status = user_game_state.bisect_interaction(lambda n: True)
    await update_bisect(user_id, user_game_state, user_game, bisect_status, update, context)


async def launch_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id, user_game, user_game_state = get_user_data(update)
    bisect_status = user_game_state.bisect_interaction(lambda n: False)
    await update_bisect(user_id, user_game_state, user_game, bisect_status, update, context)


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_messages = [
        "We're going to play \"Has rocket launched?\" Game",
        "After using /start_game for forcing restart or /get_image",
        "for getting an image (it will also start the game if it",
        "has not started) you will be asked to tell the bot if",
        "the rocket has launched or not, based on the image that",
        "the bot gives you, you will be able to choose directly",
        "from the bot response or you can use the command",
        "/rocket_launched followed by Yes or No (it is not",
        "case sensitive)",

    ]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=" ".join(help_messages)
    )


async def restart_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id, user_game, user_game_state = get_user_data(update, new_one=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Getting images, this could take few seconds"
    )
    await send_game_message(update, context, user_game_state)


def start_bot():
    pybot = RocketBot(bot_token)
    pybot.register_handler(CommandHandler('start', start))
    pybot.register_handler(CommandHandler('get_image', get_frame))
    pybot.register_handler(CommandHandler('rocket_launched', launch_response))
    pybot.register_handler(CommandHandler('Yes', launch_yes))
    pybot.register_handler(CommandHandler('No', launch_no))
    pybot.register_handler(CommandHandler('help', show_help))
    pybot.register_handler(CommandHandler('start_game', restart_game))
    pybot.run()
