class Moment():
    def __init__(self, moment_data):
        self.frame = moment_data["frame"]
        self.time = moment_data["time"]
        self.ball = moment_data["ball"]
        self.players = moment_data["players"]

    def ball_loc(self):
        return self.ball["frame"].coordinates
    
    def player_loc(self, player_id):
        for player_data in self.players:
            player = player_data["object"]
            if(str(player_id) == str(player.id)):
                return player_data["frame"].coordinates
        return None
        