import pygame
from math import atan2, cos, sin, tan, atan, acos, asin, sqrt

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Simulation")

BLUE = (100, 149, 237)
GRAY = (190, 190, 190)
EARTH_MASS = 5.9742 * 10**24
MOON_MASS = 7.36 * 10**22
SCALE = 0.02


class Planet:
    G = 6.67428 * 10**-11

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x + WIDTH / 2
        y = self.y + WIDTH / 2

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def gravity(self, objectMass: float, d: float, ball_x: float, ball_y: float) -> tuple:
        forcaGravitacional = self.G * \
            ((self.mass * objectMass) / ((d*1000000)**2))

        forcaGravitacional_x = - \
            (forcaGravitacional * cos(atan2(ball_y, ball_x)))
        forcaGravitacional_y = - \
            (forcaGravitacional * sin(atan2(ball_y, ball_x)))

        acel_x = (forcaGravitacional_x / objectMass)
        acel_y = (forcaGravitacional_y / objectMass)

        return acel_x, acel_y


class Object:
    def __init__(self, x, y, radius, mass):
        self.x_vel = 1
        self.y_vel = 0
        self.x = x
        self.y = -y
        self.radius = radius
        self.color = GRAY
        self.mass = mass

    def draw(self, win):
        x = self.x + WIDTH / 2
        y = self.y + WIDTH / 2

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def updatePosition(self, x_acel, y_acel):
        self.x_acel = x_acel
        self.y_acel = y_acel
        self.x_vel += self.x_acel
        self.y_vel += self.y_acel
        self.x += self.x_vel
        self.y += self.y_vel


def main():
    run = True
    clock = pygame.time.Clock()

    earth = Planet(0, 0, 147, BLUE, EARTH_MASS)
    ball = Object(0, 400, 30, MOON_MASS)

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        earth.draw(WIN)

        earth_image = pygame.image.load("earth-g873ef545e_640.png")
        earth_image_x = 0
        earth_image_y = 0
        WIN.blit(earth_image, (earth_image_x, earth_image_y))

        ball.draw(WIN)
        distance = sqrt(ball.x**2 + ball.y**2)
        # print(distance)
        if ball.radius + earth.radius <= distance:
            x_acel, y_acel = earth.gravity(
                objectMass=ball.mass, d=distance, ball_x=ball.x, ball_y=ball.y)
            ball.updatePosition(x_acel, y_acel)

        pygame.display.update()

    pygame.quit()


main()
