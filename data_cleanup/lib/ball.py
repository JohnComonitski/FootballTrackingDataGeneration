from lib.frame import Frame
from lib.utils import fill_gap, remove_arcs_from_path, filter_lone_points, near_by_filter
import matplotlib.pyplot as plt

class Ball():
        def __init__(self):
            self.frames = []
            self.source = None

        def add_frame(self, frame_data):
            frames = self.frames
            frames.append(Frame(frame_data))
            self.frames = frames

        def frame(self, frame_number):
            for frame in self.frames:
                if(str(frame.frame) == str(frame_number)):
                    return frame
            return None
        
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

        def clean_path(self):
            coordinates = self.path()
            filtered_coordinates = filter_lone_points(self.source, coordinates)
            filtered_coordinates = near_by_filter(self.source, filtered_coordinates)
            remaining_points = {}
            for coordinate in filtered_coordinates:
                remaining_points[str(coordinate[2])] = coordinate

            for frame in self.frames:
                frame_number = frame.frame
                if(str(frame_number) not in remaining_points):
                    empty_frame = None
                    if(self.source == "raw"):
                        empty_frame = Frame({
                            "frame" : 0,
                            "time" : 0,
                            "x" : 0,
                            "y" : 0,
                            "frame_x1" : 0,
                            "frame_y1" : 0,
                            "frame_x2" : 0,
                            "frame_y2" : 0,
                            "empty" : True
                        })
                    else:
                        empty_frame = Frame({
                            "frame" : 0,
                            "time" : 0,
                            "x" : 0,
                            "y" : 0,
                            "empty" : True
                        })
                    self.replace_frame(int(frame_number), empty_frame)

            self.fill_gaps()
            self.remove_arcs()

        def pad_start(self):
            count = 0
            for i in range(1, len(self.frames)+1):
                frame = self.frame(i)
                if frame.coordinates is None:
                    count += 1
                else:
                    for frame_number in range(1, count+1):
                        self.replace_frame(frame_number, frame)
                    return
                
        def pad_end(self):
            count = 0
            total_frames = len(self.frames)

            for frame in reversed(self.frames):
                if frame.coordinates is None:
                    count += 1
                else:
                    for i in range(count):
                        self.replace_frame(total_frames-i, frame)
                    return
                
        def fill_gaps(self):
            self.pad_start()
            self.pad_end()
            for idx in range(1, len(self.frames)):
                next_frame = self.frame(idx+1)
                if(next_frame.coordinates is None):
                    gap_size = 1
                    while(next_frame.coordinates is None):
                        next_frame = self.frame(idx + gap_size)
                        gap_size += 1
                    gap_size -= 1
                    gap_end = idx + gap_size 
                    start_frame = self.frame(idx)
                    start_coor = start_frame.coordinates
                    end_frame = self.frame(gap_end)
                    end_coor = end_frame.coordinates 
                    points = fill_gap(start_coor[0], start_coor[1], end_coor[0], end_coor[1], gap_size)
                    if(self.source == "raw"):
                        frame_1_points = fill_gap(start_frame.frame_x1, start_frame.frame_y1, end_frame.frame_x1, end_frame.frame_y1, gap_size)
                        frame_2_points = fill_gap(start_frame.frame_x2, start_frame.frame_y2, end_frame.frame_x2, end_frame.frame_y2, gap_size)
                    for i in range(1, gap_size + 1):
                        point = points[i-1]
                        tmp_frame = None
                        if(self.source == "raw"):
                            tmp_frame = Frame({
                                "frame" : idx+1,
                                "time" : 0,
                                "x" : point[0],
                                "y" : point[1],
                                "frame_x1" : frame_1_points[i-1][0],
                                "frame_y1" : frame_1_points[i-1][1],
                                "frame_x2" : frame_2_points[i-1][0],
                                "frame_y2" : frame_2_points[i-1][1],
                                "empty" : False
                            })
                        else:
                            tmp_frame = Frame({
                                "frame" : idx+1,
                                "time" : 0,
                                "x" : point[0],
                                "y" : point[1],
                                "empty" : False
                            })
                        self.replace_frame(idx+i, tmp_frame)

        def remove_arcs(self):
            path = self.path()
            coordinates = remove_arcs_from_path(path)

            for frame_number in range(1, len(coordinates)):
                frame = self.frame(frame_number)
                if(self.source == "raw"):
                    new_frame = Frame({
                        "frame" : frame.frame,
                        "time" : frame.time,
                        "x" : coordinates[frame_number][0],
                        "y" : coordinates[frame_number][1],
                        "frame_x1" : frame.frame_x1,
                        "frame_y1" : frame.frame_y1,
                        "frame_x2" : frame.frame_x2,
                        "frame_y2" : frame.frame_y2,
                        "empty" : frame.empty
                    })
                else:
                    new_frame = Frame({
                        "frame" : frame.frame,
                        "time" : frame.time,
                        "x" : coordinates[frame_number][0],
                        "y" : coordinates[frame_number][1],
                        "empty" : frame.empty
                    })
                self.replace_frame(int(frame_number), new_frame)

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
            plt.savefig('Ball Path.png', dpi=300)