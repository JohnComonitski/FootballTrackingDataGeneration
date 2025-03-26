from match import Match

match = Match()
CSV_PATH = './track/output/2e57b9_0.csv'
match.import_metrica(CSV_PATH)

# Get Ball Path
ball = match.ball
ball.clean_path()

# Merge Players
player_1 = match.player(13)
player_2 = match.player(39)
match.merge_players(player_1, player_2)

player_1 = match.player(3)
player_2 = match.player(29)
match.merge_players(player_1, player_2)

# Remove Players
player = match.player(32)
match.remove_player(player)

#Fix Teams:
player = match.player(16)
player.change_team(1)
player = match.player(33)
player.change_team(1)

match.export()