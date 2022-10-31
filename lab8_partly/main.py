import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))


def draw_body(surface, x, y, size, color):
    circle(surface, color, (x, y), size // 2)


def draw_eye(surface, x, y, size, color):
    circle(surface, color, (x, y), size // 2)


def draw_zr(surface, x, y, size, color):
    circle(surface, color, (x, y), size // 2)


def draw_moth(screen, left, top, width, height, color):
    rect(screen, color, (left, top, width, height))


def draw_br(screen, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, color):
    polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)])


def draw_smile(surface, x, y, size, color_body, color_eye, color_zr, color_br):

    draw_body(surface, x, y, size, color_body)

    eye_size = 3 * size // 10
    x_eye1 = x - size // 5
    y_eye1 = y - size // 9
    draw_eye(surface, x_eye1, y_eye1, eye_size, color_eye)

    eye_size = 3 * size // 14
    x_eye2 = x + 6 * size // 25
    y_eye2 = y - size // 9
    draw_eye(surface, x_eye2, y_eye2, eye_size, color_eye)

    zr_size1 = size // 10
    draw_zr(surface, x_eye1, y_eye1, zr_size1, color_zr)
    zr_size2 = size // 14
    draw_zr(surface, x_eye2, y_eye2, zr_size2, color_zr)

    width = size // 2
    height = size // 10
    y_moth = y + size // 4
    x_moth = x - width // 2
    draw_moth(screen, x_moth, y_moth, width, height, color_zr)

    x1 = x // 2
    y1 = y // 2
    x2 = x1 + size // 20
    y2 = y1 - size // 20
    x3 = x - size // 10
    y3 = y - size // 5
    x4 = x3 + size // 20
    y4 = y3 - size // 20
    draw_br(screen, x1, y1, x2, y2, x4, y4, x3, y3, x1, y1, color_br)

    x1 = 3 * x // 2
    y1 = y // 2 + y // 15
    x2 = x1 + size // 20
    y2 = y1 + size // 20
    x3 = x + size // 10
    y3 = y - size // 5
    x4 = x3 - size // 20
    y4 = y3 - size // 20
    draw_br(screen, x1, y1, x2, y2, x3, y3, x4, y4, x1, y1, color_br)


draw_smile(screen, 200, 200, 200, (255, 255, 0), (220, 20, 60), (0, 0, 0), (255, 105, 180))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
