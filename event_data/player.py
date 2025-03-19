from frame import Frame
import matplotlib.pyplot as plt

class Player():
        def __init__(self, player_data):
            self.id = player_data["id"]
            self.team = player_data["team"]
            self.name = player_data["name"]
            self.frames = []
            self.source = None

        def change_team(self, team):
            self.team = team

        def change_name(self, name):
            self.name = name
            
        def add_frame(self, frame_data):
            if(str(type(frame_data)) == "<class 'frame.Frame'>"):
                frames = self.frames
                frames.append(frame_data)
                self.frames = frames
            else:
                frames = self.frames
                frames.append(Frame(frame_data))
                self.frames = frames

        def frame(self, frame_number):
            for frame in self.frames:
                if(str(frame.frame) == str(frame_number)):
                    return frame
            return None
        
        def still_exist_after_frame(self, frame_number):
            for frame in self.frames[(frame_number+1):]:
                if frame.exists:
                    return True
            return False
        
        def last_frame(self):
            last_frame = 0
            for i in range(len(self.frames)):
                if self.frames[i].exists:
                    last_frame = i
            return last_frame
        
        def path(self):
            path = []
            frame_number = 1
            for frame in self.frames:
                coor = frame.coordinates
                if coor:
                    path.append((coor[0], coor[1], frame_number))
                else:
                    path.append((0, 0, frame_number))
                frame_number += 1
            return path
        
        def replace_frame(self, frame_number, new_frame):
            frame = self.frame(frame_number)

            if(self.source == "raw"):
                self.frames[frame_number - 1] = Frame({
                    "frame" : frame_number,
                    "time" : frame.time,
                    "x" : new_frame.x,
                    "y" : new_frame.y,
                    "frame_x1" : new_frame.frame_x1,
                    "frame_y1" : new_frame.frame_y1,
                    "frame_x2" : new_frame.frame_x2,
                    "frame_y2" : new_frame.frame_y2,
                    "empty" : new_frame.empty
                })
            else:
                self.frames[frame_number - 1] = Frame({
                    "frame" : frame_number,
                    "time" : frame.time,
                    "x" : new_frame.x,
                    "y" : new_frame.y,
                    "empty" : new_frame.empty
                })

        def plot(self):
            coordinates = self.path()
            x_values, y_values, z_values = zip(*coordinates) if coordinates else ([], [], [])

            norm = plt.Normalize(min(z_values), max(z_values))
            cmap = plt.cm.viridis

            plt.figure(figsize=(6, 4))
            plt.scatter(x_values, y_values, c=z_values, cmap=cmap, norm=norm, marker='o')

            plt.title("Ball Path")
            plt.grid(True)
            plt.gca().invert_yaxis()
            plt.savefig(self.name + ' Path.png', dpi=300)