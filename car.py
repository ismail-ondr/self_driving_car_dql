import pygame
from radar import Radar
import random
import math


class Car:
    def __init__(self, screen, start_point):
        self.pos_x, self.pos_y = start_point
        self.car_speed = 5
        self.width, self.height = 50, 30
        self.color = (0, 128, 255)
        self.rotation_angle = random.randint(-30, 30)
        self.screen = screen
        self.radar_max_length = 200

        self.radars = []
        self.radar_measurements = []
        self.calculate_radar_measurements()

    def draw(self):
        self.pos_y -= self.car_speed * math.sin(math.radians(self.rotation_angle))
        self.pos_x += self.car_speed * math.cos(math.radians(self.rotation_angle))

        rotated_rect = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(rotated_rect, self.color, (0, 0, self.width, self.height))
        rotated_rect = pygame.transform.rotate(rotated_rect, self.rotation_angle)
        rect_rect = rotated_rect.get_rect(center=(self.pos_x, self.pos_y))
        self.screen.blit(rotated_rect, rect_rect.topleft)

        self.calculate_radar_measurements()
        self.draw_radars()

    def draw_radars(self):

        for radar in self.radars:
            pygame.draw.line(self.screen, (0, 0, 255, 0), (radar.start_pos_x, radar.start_pos_y),
                             (radar.end_pos_x, radar.end_pos_y), 2)
            pygame.draw.circle(self.screen, (0, 255, 0, 0), (radar.end_pos_x, radar.end_pos_y), 2)

    def get_radar_start_points(self):

        top_mid_x = self.pos_x + (self.width / 2) * math.cos(math.radians(self.rotation_angle))
        top_mid_y = self.pos_y - (self.width / 2) * math.sin(math.radians(self.rotation_angle))
        pygame.draw.circle(self.screen, (0, 255, 0, 0), (top_mid_x, top_mid_y), 2)

        top_left_x = top_mid_x + (self.height / 2) * math.cos(math.radians(self.rotation_angle + 90))
        top_left_y = top_mid_y - (self.height / 2) * math.sin(math.radians(self.rotation_angle + 90))
        pygame.draw.circle(self.screen, (0, 255, 0, 0), (top_left_x, top_left_y), 2)

        top_right_x = top_mid_x + (self.height / 2) * math.cos(math.radians(self.rotation_angle - 90))
        top_right_y = top_mid_y - (self.height / 2) * math.sin(math.radians(self.rotation_angle - 90))
        pygame.draw.circle(self.screen, (0, 255, 0, 0), (top_right_x, top_right_y), 2)

        center_left_x = self.pos_x + (self.height / 2) * math.cos(math.radians(self.rotation_angle + 90))
        center_left_y = self.pos_y - (self.height / 2) * math.sin(math.radians(self.rotation_angle + 90))
        pygame.draw.circle(self.screen, (0, 255, 0, 0), (center_left_x, center_left_y), 2)

        center_right_x = self.pos_x + (self.height / 2) * math.cos(math.radians(self.rotation_angle - 90))
        center_right_y = self.pos_y - (self.height / 2) * math.sin(math.radians(self.rotation_angle - 90))
        pygame.draw.circle(self.screen, (0, 255, 0, 0), (center_right_x, center_right_y), 2)

        return [(top_left_x, top_left_y), (top_left_x, top_left_y), (top_mid_x, top_mid_y),
                (top_right_x, top_right_y),  (top_right_x, top_right_y)]

    def calculate_radar_measurements(self):
        angle = 90
        self.radars.clear()
        self.radar_measurements.clear()
        for radar_start_point in self.get_radar_start_points():
            radar_length = 0
            start_x, start_y = radar_start_point
            end_x, end_y = radar_start_point
            while (not self.screen.get_at((int(end_x), int(end_y))) == pygame.Color(0, 0, 0)
                   and radar_length < self.radar_max_length):
                radar_length += 1
                end_x = start_x + math.cos(math.radians(self.rotation_angle + angle)) * radar_length
                end_y = start_y - math.sin(math.radians(self.rotation_angle + angle)) * radar_length

            radar = Radar(start_x, start_y, end_x, end_y)
            self.radars.append(radar)
            self.radar_measurements.append(radar.distance / self.radar_max_length)
            angle -= 45

    def is_crash(self):
        return any(item.distance <= 5 for item in self.radars)

    def get_radars(self):
        return self.radars.copy()

    def get_radar_measurements(self):
        return self.radar_measurements
