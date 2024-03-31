from car import Car
import pygame
import sys


class Environment:
    def __init__(self, keyboard_control=True):
        pygame.init()

        self.width, self.height = 1250, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Self Driving Car")

        self.background_image = pygame.transform.scale(pygame.image.load("resources/path1.png"),
                                                       (self.width, self.height))

        self.clock = pygame.time.Clock()

        self.car = Car(self.screen)

        self.keyboard_control = keyboard_control
        self.action_space = [
            0,     # left
            1,      # straight
            2       # right
        ]

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
        reward = 3
        if action == 0:
            self.car.rotation_angle += 5
        elif action == 1:
            reward += 1
            pass
        elif action == 2:
            self.car.rotation_angle -= 5

        self.render()
        return self.get_observation_space(), reward, self.car.is_crash()



    def render(self):
        self.screen.fill((255, 255, 255))  # Beyaz arka plan
        self.screen.blit(self.background_image, (0, 0))
        self.car.draw()

        if self.car.is_crash():
            self.reset()
        # print(pygame.mouse.get_pos())
        pygame.display.flip()

    def reset(self):
        self.car = Car(self.screen)
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
            self.clock.tick(30)
