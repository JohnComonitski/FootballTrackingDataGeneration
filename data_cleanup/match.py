from moment import Moment
from player import Player
from ball import Ball
import csv

class Match():
    def __init__(self):
        self.players = []
        self.ball = Ball()
        self.current_frame = 1
        self.frames = 0
        self.source = None

    def import_metrica(self, path):
        self.source = "metrica"
        headers = []
        frames = []
        with open(path, "r") as file:
            count = 0
            for line in file:
                if count < 3:
                    headers.append(line.strip().split(","))
                else:
                    frames.append(line.strip().split(","))
                count += 1
                
        team_row = headers[0]
        player_id_row = headers[1]
        player_row = headers[2]

        players = []
        ball_idx = 0
        for i in range(3, len(headers[0]), 2):
            if(player_row[i] == "Ball"):
                ball_idx = i
            else:
                players.append(Player({
                    "team" : team_row[i],
                    "id" : player_id_row[i],
                    "name" : player_row[i],
                }))
        
        self.frames = len(frames)
        for frame in frames:
            player_count = 0
            for i in range(3, len(frame), 2):
                frame_data = {
                    "frame" : frame[1],
                    "time" : frame[2]
                }
                if frame[i] == "0" or frame[i+1] == "0":
                    frame_data["empty"] = True
                else:
                    frame_data["x"] = frame[i]
                    frame_data["y"] = frame[i+1]

                if(i == ball_idx):
                    self.ball.source = "metrica"
                    self.ball.add_frame(frame_data)
                else:
                    players[player_count].source = "metrica"
                    players[player_count].add_frame(frame_data)
                    player_count += 1
        self.players = players

    def import_raw_data(self, path):
        self.source = "raw"
        frames = []
        with open(path, "r") as file:
            for line in file:
                    frames.append(line.strip().split(","))
        frames = frames[1:]
        
        players = {}
        for frame in frames:
            frame_number = int(frame[0])
            obj = frame[1]

            frame_data = {
                "frame" : frame_number,
                "time" : frame_number / 24
            }

            if frame[8] == "0" or frame[9] == "0":
                frame_data["empty"] = True
            else:
                frame_data["frame_x1"] = frame[4]
                frame_data["frame_y1"] = frame[5]
                frame_data["frame_x2"] = frame[6]
                frame_data["frame_y2"] = frame[7]
                frame_data["x"] = frame[8]
                frame_data["y"] = frame [9]

            if(obj == "ball"):
                self.ball.source = "raw"
                self.ball.add_frame(frame_data)
                self.frames = self.frames + 1
            else:
                player_id = frame[2]
                team = float(frame[3])
                if( str(player_id) not in players):
                    players[str(player_id)] = Player({
                        "team" : team,
                        "id" : player_id,
                        "name" : "Player " + str(player_id),
                    })
                    
                player = players[str(player_id)]
                player.source = "raw"
                player.add_frame(frame_data)

        self.players = []
        for player_id in players:
            player = players[player_id]
            self.players.append(player)

    def player(self, player_id):
        for player in self.players:
            if(str(player_id) == str(player.id)):
                return player
            
        return None
    
    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        for i in range(len(self.players)):
            if str(self.players[i].id) == str(player.id):
                return self.players.pop(i)
    
    def team(self, team):
        players = []
        for player in self.players:
            if(player.team == team):
                players.append(player)
        return players
    
    def merge_players(self, player1, player2):
        new_player = Player({
            "id" : player1.id,
            "team" : player1.team,
            "name" : player1.name,
        })

        for frame_number in range(1, self.frames+1):
            player1_frame = player1.frame(frame_number)
            player2_frame = player2.frame(frame_number)
            if(player1_frame):
                new_player.add_frame(player1_frame)
            elif(player2_frame):
                new_player.add_frame(player2_frame)

        self.remove_player(player1)
        self.remove_player(player2)
        self.add_player(new_player)

        return new_player
    
    def frame(self, frame_number):
        if(frame_number > self.frames):
            return None
        
        ball_frame = self.ball.frame(frame_number)
        ball = {
            "object" : self.ball,
            "type" : "Ball",
            "frame" : ball_frame
        }

        players = []
        for player in self.players:
            players.append({
                "object" : player,
                "type" : "Player",
                "frame" : player.frame(frame_number)
            })

        return Moment({
            "ball" : ball,
            "players" : players,
            "frame" : ball_frame.frame,
            "time" : ball_frame.time
        })
    
    def has_next_frame(self):
        moment = self.frame(self.current_frame + 1)
        if moment == None:
            return False
        return True
    
    def next_frame(self):
        self.current_frame = self.current_frame + 1
        return self.frame(self.current_frame)
    
    def first_frame(self):
        self.current_frame = 1
        return self.frame(self.current_frame)
    
    def export(self):
        data = []
        if(self.source == "metrica"):
            data = self.__export_metrica()
        elif(self.source == "raw"):
            data = self.__export_raw()

        csv_writer = csv.writer(open('match_data.csv', 'w', newline='\n'))
        csv_writer.writerows(data)

    def __export_metrica(self):
        header = []
        header_row1 = ["","",""]
        header_row2 = ["","",""]
        header_row3 = ["Period","Frame","Time [s]"]
        for player in self.players:
            header_row1.append(player.team)
            header_row1.append("")
            header_row2.append(player.id)
            header_row2.append("")
            header_row3.append(player.name)
            header_row3.append("")
        header_row1.append("")
        header_row2.append("")
        header_row3.append("Ball")
        header_row3.append("")
        header.append(header_row1)
        header.append(header_row2)
        header.append(header_row3)

        data = []
        ball = self.ball
        for frame_number in range(1, self.frames + 1):
            row = []
            row.append(1)
            row.append(frame_number)
            row.append(frame_number * .04)
            for player in self.players:
                frame = player.frame(frame_number)
                if(frame):
                    coordinates = frame.coordinates
                    if(coordinates):
                        row.append(coordinates[0])
                        row.append(coordinates[1])
                    else:
                        row.append(0)
                        row.append(0)   
                else:
                    row.append(0)
                    row.append(0)      

            
            coordinates = ball.frame(frame_number).coordinates
            if(coordinates):
                row.append(coordinates[0])
                row.append(coordinates[1])
            else:
                row.append(0)
                row.append(0)
            data.append(row)


        return header + data
    
    def __export_raw(self):
        header = [[ "Frame", "Object", "Object ID", "Team", "X1", "Y1", "X2", "X2", "X_Pitch", "Y_Pitch" ]]
        data = []

        moment = self.first_frame()
        ball = moment.ball["frame"]
        for player in moment.players:
            frame = player["frame"]
            if(frame):
                player = player["object"]
                data.append([moment.frame, "player", player.id, player.team, frame.frame_x1, frame.frame_y1, frame.frame_x2, frame.frame_y2, frame.x, frame.y ])
        data.append([moment.frame, "ball", 0, 0, ball.frame_x1, ball.frame_y1, ball.frame_x2, ball.frame_y2, ball.x, ball.y ])
        
        while(self.has_next_frame()):
            moment = self.next_frame()
            ball = moment.ball["frame"]
            for player in moment.players:
                frame = player["frame"]
                if(frame):
                    player = player["object"]
                    data.append([moment.frame, "player", player.id, player.team, frame.frame_x1, frame.frame_y1, frame.frame_x2, frame.frame_y2, frame.x, frame.y ])
            data.append([moment.frame, "ball", 0, 0, ball.frame_x1, ball.frame_y1, ball.frame_x2, ball.frame_y2, ball.x, ball.y ])

        return header + data