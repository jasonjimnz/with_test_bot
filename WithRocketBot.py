from telegram.ext import ApplicationBuilder, Application


class RocketBot(object):
    tg_bot: Application = None

    def __init__(self, bot_token: str):
        self.tg_bot = self.init_bot(bot_token)

    @classmethod
    def init_bot(cls, bot_token: str) -> Application:
        return ApplicationBuilder().token(bot_token).build()

    def register_handler(self, command_handler, bot_instance: Application = None):
        if bot_instance:
            bot_instance.add_handler(command_handler)
        else:
            self.tg_bot.add_handler(command_handler)

    def run(self):
        self.tg_bot.run_polling()
