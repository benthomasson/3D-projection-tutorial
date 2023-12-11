
import cairo
import subprocess
import math

WIDTH, HEIGHT = 800, 600
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Create cairo surface
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

command = "ffmpeg -y -f rawvideo -vcodec rawvideo -s 800x600 -pix_fmt bgra -r 60 -i - -threads 0 -preset fast -an -vcodec libx264 -crf 21 -pix_fmt yuv420p -f mp4 output.mp4"
command = command.split(" ")

writing_process = subprocess.Popen(command, stdin=subprocess.PIPE)

frame = 0
done = False
while not done:
    frame += 1
    print(frame)

    # Draw background
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.set_source_rgb(*WHITE)
    ctx.fill()


    # Draw a red circle
    ctx.arc(WIDTH/2, HEIGHT/2, 100, 0, 2*math.pi)
    ctx.set_source_rgb(*BLUE)
    ctx.fill()

    writing_process.stdin.write(surface.get_data())

    if frame > 100:
        done = True

writing_process.stdin.close()
writing_process.wait()

