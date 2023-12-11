from math import *

import numpy as np
import pygame
from scipy.interpolate import interp1d
import os

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 1024, 768
pygame.display.set_caption(
    os.path.splitext(os.path.basename(__file__))[0].replace("_", " ").title()
)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 1

circle_pos = [WIDTH / 2, HEIGHT / 2]  # x, y

angle = 0


def polar2z(r, theta):
    return r * np.exp(1j * theta)


def z2polar(z):
    return (np.abs(z), np.angle(z))


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return (rho, phi)


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)


def radians(degrees):
    return degrees * np.pi / 180


circle_points = []

GENERATIONS = 10
TIME_SCALE = 20
REPLICATION_RATE = 2

red_space = np.linspace(0, 255, GENERATIONS)
blue_space = np.linspace(255, 0, GENERATIONS)

MASSES = [0]


def point_offset(i, j, num_points):
    # return ((i * (i-num_points)) / (num_points * num_points)) - 0.1
    # return 0 if i == 0 1
    # return 0.1 * (i - num_points / 2) / num_points
    # linear centered on 0
    print(i * (num_points - i) / (num_points * num_points) * 4)
    return i * (num_points - i) / (num_points * num_points) * 4
    # return (
    #    i
    #    * i
    #    * (i - num_points)
    #    * (i - num_points)
    #    * (i - num_points / 2)
    #    * (i - num_points / 2)
    #    / (num_points * num_points * num_points * num_points * num_points * num_points)
    #    * 512
    # )


def simulate_masses(masses, num_points):
    initial = [1 for _ in range(num_points)]
    final = initial.copy()
    for mass, offset in masses:
        final[mass] = offset
        for j in range(10):
            for i in range(int(num_points / 2)):
                final[(mass + i + 1) % num_points] = min(
                    [
                        final[(mass + i + 1) % num_points],
                        (
                            final[(mass + i) % num_points]
                            + final[(mass + i + 2) % num_points]
                        )
                        / 2,
                    ]
                )
                final[(mass - i - 1) % num_points] = min(
                    [
                        final[(mass - i - 1) % num_points],
                        (
                            final[(mass - i) % num_points]
                            + final[(mass - i - 2) % num_points]
                        )
                        / 2,
                    ]
                )
    print(final)
    return final


num_points = 1
for j in range(0, GENERATIONS):
    print(num_points)
    rad_space = np.linspace(0, 360, num_points + 1)
    if num_points >= 4:
        masses = [
            (0, 0.75),
            (num_points // 64, 0.5),
            #(3 * num_points // 4, 0.5),
            #(num_points // 4, 0.5),
            #(num_points // 2, 0.5),
        ]
    else:
        masses = [(0, 0.5)]
    offsets = simulate_masses(masses, num_points)
    for i in range(num_points):
        phi = radians(rad_space[i])
        circle_points.append(
            (
                np.matrix(
                    [
                        *pol2cart(offsets[i] * num_points, phi),
                        # *pol2cart(point_offset(i, j, num_points) * num_points, phi),
                        j * TIME_SCALE,
                    ]
                ),
                BLACK if i == 0 else (red_space[j], 0, blue_space[j]),
            )
        )
        circle_points.append(
            (
                np.matrix(
                    [
                        *pol2cart(num_points, phi),
                        j * TIME_SCALE,
                    ]
                ),
                GREEN,
            )
        )
    num_points = ceil(REPLICATION_RATE * num_points)

points = circle_points

projection_matrix = np.matrix(
    [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
)


projected_points = [[n, n] for n in range(len(points))]


clock = pygame.time.Clock()
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # update stuff

    rotation_z = np.matrix(
        [
            [cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1],
        ]
    )

    rotation_y = np.matrix(
        [
            [cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)],
        ]
    )

    rotation_x = np.matrix(
        [
            [1, 0, 0],
            [0, cos(angle), -sin(angle)],
            [0, sin(angle), cos(angle)],
        ]
    )
    angle += 0.01

    screen.fill(BLACK)
    # drawining stuff

    i = 0
    for point, color in points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, color, (x, y), 2)
        i += 1

    pygame.display.update()
