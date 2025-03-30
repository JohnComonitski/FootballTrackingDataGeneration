class Frame():
        def __init__(self, frame_data):
            self.frame = frame_data["frame"]
            self.time = frame_data["time"]
            if "empty" in frame_data and frame_data["empty"]:
                self.empty = True
                self.x = None
                self.y = None
                self.frame_x1 = None
                self.frame_y1 = None
                self.frame_x2 = None
                self.frame_y2 = None
                self.coordinates = None
            else:
                self.empty = False
                self.x = float(frame_data["x"])
                self.y = float(frame_data["y"])
                self.frame_x1 = None
                self.frame_y1 = None
                self.frame_x2 = None
                self.frame_y2 = None
                self.coordinates = (float(frame_data["x"]), float(frame_data["y"]))
                if( "frame_x1" in frame_data ):
                    self.frame_x1 = frame_data["frame_x1"]
                    self.frame_y1 = frame_data["frame_y1"]
                    self.frame_x2 = frame_data["frame_x2"]
                    self.frame_y2 = frame_data["frame_y2"]
