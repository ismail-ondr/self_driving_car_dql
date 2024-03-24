import pygame
from car import Car
import sys


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":

    pygame.init()

    width, height = 1250, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Self Driving Car")

    background_image = pygame.transform.scale(pygame.image.load("resources/path1.png"), (width, height))

    clock = pygame.time.Clock()

    car = Car(screen)
    while True:
        handle_events()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            car.car_speed = 5
        elif keys[pygame.K_DOWN]:
            car.car_speed = -5
        else:
            car.car_speed = 0
        if keys[pygame.K_LEFT]:
            car.rotation_angle += 5
        elif keys[pygame.K_RIGHT]:
            car.rotation_angle -= 5

        screen.fill((255, 255, 255))
        screen.blit(background_image, (0, 0))
        car.update()
        car.draw()

        pygame.display.flip()
        clock.tick(30)
