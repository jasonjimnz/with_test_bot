import datetime


class BotHandler(object):
    active_users = dict()

    def get_user_game(self, user_id: str) -> dict:
        if self.active_users.get(user_id):
            return self.active_users.get(user_id)
        else:
            self.active_users[user_id] = {
                "updated_at": None,
                "awaiting_response": False,
                "state": {
                    "left": None,
                    "right": None,
                    "total_elements": None,
                    "mapper": None
                }
            }
            return self.active_users[user_id]

    def set_user_game(self, user_id: str, game_state: dict):
        user_game = self.get_user_game(user_id)
        user_game['state'] = game_state
        user_game['updated_at'] = datetime.datetime.now().isoformat()
        self.active_users[user_id] = user_game


def game_validator(response: str):
    return response.lower() in ['yes', 'y', 'true']
