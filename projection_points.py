import pygame
import numpy as np
from math import *
from scipy.interpolate import interp1d

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100

circle_pos = [WIDTH/2, HEIGHT/2]  # x, y

angle = 0


def polar2z(r,theta):
    return r * np.exp( 1j * theta )

def z2polar(z):
    return ( np.abs(z), np.angle(z) )

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def radians(degrees):
    return degrees * np.pi / 180

circle_points = []

generations = 20
nodes = 8

red_space = np.linspace(255, 0, generations)
blue_space = np.linspace(0, 0, generations)


circle_points.append((np.matrix([0, 0, 0]), (255,0,0), 20))

for j in range(0, generations):
    j = float(j) / (1.0  * generations)
    for i in range(0, 360, 360//nodes):
        circle_points.append((np.matrix([*pol2cart(j*j, radians(i)), j]),
                              (red_space[int(j*10)], 0, blue_space[int(j*10)]),
                              5))

points = circle_points

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
])


projected_points = [
    [n, n] for n in range(len(points))
]



clock = pygame.time.Clock()
while True:

    clock.tick(60)
    print(clock.get_fps())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # update stuff

    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    angle += 0.01

    screen.fill(BLACK)
    # drawining stuff

    i = 0
    for point, color, size in points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, color, (x, y), size)
        i += 1

    pygame.display.update()
