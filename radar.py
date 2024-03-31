
import math


class Radar:

    def __init__(self, start_pos_x, start_pos_y, end_pos_x, end_pos_y):
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.end_pos_x = end_pos_x
        self.end_pos_y = end_pos_y
        self.distance = math.sqrt((self.end_pos_x - self.start_pos_x) ** 2 + (self.end_pos_y - self.start_pos_y) ** 2)
