
import pygame
import subprocess

WIDTH, HEIGHT = 800, 600
RED = (255, 0, 0)
WHITE = (255, 255, 255)
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

command = "ffmpeg -y -f rawvideo -vcodec rawvideo -s 800x600 -pix_fmt rgba -r 60 -i - -threads 0 -preset fast -an -vcodec libx264 -crf 21 -pix_fmt yuv420p -f mp4 output.mp4"
command = command.split(" ")

writing_process = subprocess.Popen(command, stdin=subprocess.PIPE)

clock = pygame.time.Clock()
frame = 0
done = False
while not done:
    frame += 1
    print(frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                done = True
                break
    if done:
        break

    clock.tick(60)
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (400, 300), 50)

    writing_process.stdin.write(pygame.image.tobytes(screen, 'RGBA'))
    pygame.display.update()

writing_process.stdin.close()
writing_process.wait()

