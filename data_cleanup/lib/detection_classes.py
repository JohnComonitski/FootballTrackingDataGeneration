import numpy as np

class Coordinate:
  def __init__(self, x1, y1, x2, y2):
    self._data = np.array([float(x1), float(y1), float(x2), float(y2)])

  def __iter__(self):
    for elem in self._data:
      yield elem

  def get_anchors_coordinates(self):
    return  np.array([self._data[0], self._data[1]])

  def astype(self, type):
    return int(self._data[0]), int(self._data[1]), int(self._data[2]), int(self._data[3])


class Detections:
    def __init__(self, xyxy, class_id):
        self.xyxy = xyxy
        self.class_id = class_id

    def __len__(self):
      return len(self.xyxy)

    def get_anchors_coordinates(self, anchor):
      tmp = []
      for coord in self.xyxy:
        arr = np.array([int(coord._data[0]), int(coord._data[1])])
        tmp.append(arr)
      return np.array(tmp)

class Rect:
    def __init__(self, x, y, length, height):
        self.x = x
        self.y = y
        self.length = length
        self.width = length
        self.height = height