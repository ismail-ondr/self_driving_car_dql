import pygame
import random
import math


class Car:
    def __init__(self, screen):
        self.pos_x, self.pos_y = 490, 562
        self.car_speed = 5
        self.width, self.height = 50, 30
        self.color = (0, 128, 255)
        self.rotation_angle = random.randint(-30, 30)
        self.screen = screen

    def update(self):
        self.pos_y -= self.car_speed * math.sin(math.radians(self.rotation_angle))
        self.pos_x += self.car_speed * math.cos(math.radians(self.rotation_angle))

    def draw(self):
        rotated_rect = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(rotated_rect, self.color, (0, 0, self.width, self.height))
        rotated_rect = pygame.transform.rotate(rotated_rect, self.rotation_angle)
        rect_rect = rotated_rect.get_rect(center=(self.pos_x, self.pos_y))
        self.screen.blit(rotated_rect, rect_rect.topleft)


