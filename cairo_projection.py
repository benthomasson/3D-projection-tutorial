import subprocess
from math import cos, pi, sin

import cairo
import numpy as np

WIDTH, HEIGHT = 1920, 1080
FPS = 60
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create cairo surface
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

command = f"ffmpeg -y -f rawvideo -vcodec rawvideo -s {WIDTH}x{HEIGHT} -pix_fmt bgra -r {FPS} -i - -threads 0 -preset fast -an -vcodec libx264 -crf 21 -pix_fmt yuv420p -f mp4 output.mp4"
command = command.split(" ")

writing_process = subprocess.Popen(command, stdin=subprocess.PIPE)

scale = 100

circle_pos = [WIDTH / 2, HEIGHT / 2]  # x, y

angle = 0

points = []

# all the cube vertices
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1, 1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))


projection_matrix = np.matrix(
    [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
)


projected_points = [[n, n] for n in range(len(points))]


def connect_points(ctx, i, j, points):
    ctx.set_source_rgb(*WHITE)
    ctx.set_line_width(2)
    ctx.move_to(points[i][0], points[i][1])
    ctx.line_to(points[j][0], points[j][1])
    ctx.stroke()


frame = 0
done = False
while not done:
    frame += 1

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

    # Draw background
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.set_source_rgb(*BLACK)
    ctx.fill()

    # drawing stuff

    i = 0
    for point in points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        # Draw a red circle
        ctx.arc(x, y, 5, 0, 2 * pi)
        ctx.set_source_rgb(*RED)
        ctx.fill()
        i += 1

    for p in range(4):
        connect_points(ctx, p, (p + 1) % 4, projected_points)
        connect_points(ctx, p + 4, ((p + 1) % 4) + 4, projected_points)
        connect_points(ctx, p, (p + 4), projected_points)

    writing_process.stdin.write(surface.get_data())

    if frame > 1000:
        done = True

writing_process.stdin.close()
writing_process.wait()
