from car import Car
import pygame
import sys
import random


class Environment:
    def __init__(self, keyboard_control=True):
        pygame.init()

        self.width, self.height = 1250, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Self Driving Car")

        self.paths = ["resources/path1.png", "resources/path2.png"]
        self.start_points = [(490, 562), (710, 575)]

        index = random.randint(0, 1)
        self.background_image = pygame.transform.scale(pygame.image.load(self.paths[index]),
                                                       (self.width, self.height))

        self.car = Car(self.screen, self.start_points[index])

        self.keyboard_control = keyboard_control
        self.action_space = [
            0,      # left
            1,      # straight
            2       # right
        ]

        self.clock = pygame.time.Clock()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def handle_keyboard_actions(self):
        if self.keyboard_control:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.car.car_speed = 5
            elif keys[pygame.K_DOWN]:
                self.car.car_speed = -5
            else:
                self.car.car_speed = 0
            if keys[pygame.K_LEFT]:
                self.car.rotation_angle += 5
            elif keys[pygame.K_RIGHT]:
                self.car.rotation_angle -= 5

    def update(self, action):
        reward = 5
        if action == 0:
            self.car.rotation_angle += 5

        elif action == 2:
            self.car.rotation_angle -= 5

        self.render()
        if self.car.is_crash():
            reward = -10
        return self.get_observation_space(), reward, self.car.is_crash()



    def render(self):
        self.screen.fill((255, 255, 255))  # Beyaz arka plan
        self.screen.blit(self.background_image, (0, 0))
        self.car.draw()

        # if self.car.is_crash():
        #     self.reset()
        # print(pygame.mouse.get_pos())
        pygame.display.flip()
        self.clock.tick(20)

    def reset(self):
        index = random.randint(0, 1)
        self.background_image = pygame.transform.scale(pygame.image.load(self.paths[index]),
                                                       (self.width, self.height))

        self.car = Car(self.screen, self.start_points[index])
        return self.get_observation_space()

    def get_observation_space(self):
        return self.car.get_radar_measurements().copy()

    def get_action_space(self):
        return self.action_space

    def run(self):
        while True:
            self.handle_events()

            self.handle_keyboard_actions()
            self.render()

