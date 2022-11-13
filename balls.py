import pygame
from pygame.draw import *
from random import randint
pygame.init()

# Некоторые базовые константы
FPS = 60
SCREEN_LENGTH = 1366
SCREEN_WIDTH = 768
BALL_NUMBER = 5
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))

#Константы цветов
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

#Массивы атрибутов шаров
ball_x = [0 for i in range(BALL_NUMBER)]
ball_y = [0 for i in range(BALL_NUMBER)]
ball_r = [0 for i in range(BALL_NUMBER)]
ball_vx = [0 for i in range(BALL_NUMBER)]
ball_vy = [0 for i in range(BALL_NUMBER)]
ball_color = [0 for i in range(BALL_NUMBER)]

#Атрибуты, ответственные за подсчет шаров
score = 0

def new_ball(i: int):
    ball_x[i] = randint(100, SCREEN_LENGTH - 100)
    ball_vx[i] = randint(-10, 11)
    ball_y[i] = randint(100, SCREEN_WIDTH - 100)
    ball_vy[i] = randint(-10, 11)
    ball_r[i] = randint(10, 100)
    ball_color[i] = COLORS[randint(0, 5)]
    circle(screen, ball_color[i], (ball_x[i], ball_y[i]), ball_r[i])

def click(event):
    global score

    for i in range(BALL_NUMBER):
        if (event.pos[0] - ball_x[i])**2 + (event.pos[1] - ball_y[i])**2 <= ball_r[i]**2:
            circle(screen, BLACK, (ball_x[i], ball_y[i]), ball_r[i])
            new_ball(i)
            score+=1

def move_ball(i: int):
    """"
     Процедура, перемещающая шар
     :param i: Порядок номера шара
    """
    circle(screen, BLACK, (ball_x[i], ball_y[i]), ball_r[i])
    if (ball_x[i] - ball_r[i]) <= 0 or (ball_x[i] + ball_r[i]) >= SCREEN_LENGTH:
        ball_vx[i] = -ball_vx[i]
    if (ball_y[i] - ball_r[i]) <= 0 or (ball_y[i] + ball_r[i]) >= SCREEN_WIDTH:
        ball_vy[i] = -ball_vy[i]
    ball_x[i] += ball_vx[i]
    ball_y[i] += ball_vy[i]
    circle(screen, ball_color[i], (ball_x[i], ball_y[i]), ball_r[i])

def score_points(score: int):
    """
    Выводит на экран количество набранных очков
    :param score:
    """
    f = pygame.font.Font(None, 36)
    text = f.render('Score: ' +str(score-1), True, (0, 0, 0))
    screen.blit(text, (24, 18))
    text = f.render('Score: ' +str(score), True, (0, 200, 0))
    screen.blit(text, (24, 18))

#Генерация начальных условий игры
pygame.display.update()
clock = pygame.time.Clock()
finished = False
for i in range(BALL_NUMBER):
    new_ball(i)

#Основной цикл, обрабатывающий события
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    for i in range(BALL_NUMBER):
        move_ball(i)
    score_points(score)
    pygame.display.update()

pygame.quit()
