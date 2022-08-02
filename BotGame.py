
class BotServer(object):
    active_games = {}

    def start_game(self, user_id: str):
        self.active_games[user_id] = {
            "is_started": False,
            "current_frame": None,
            "highest_frame": None,
            "lowest_frame": None,
            "finished_at": None
        }

    def update_game(self, user_id: str, user_dict: dict):
        if self.active_games.get(user_id):
            self.active_games[user_id] = user_dict
            return True
        return False
