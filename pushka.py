# python3 gun.py

import math
from random import choice
from random import randint

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRAVITY_TENSION = 1


class Object:
    def __init__(self, screen: pygame.Surface, x, y, vx, vy):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self, gravity=0):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if (self.x - self.r) <= 0 or (self.x + self.r) >= SCREEN_WIDTH:
            self.vx = -self.vx
            self.x += self.vx
        if (self.y - self.r) <= 0 or (self.y + self.r) >= SCREEN_HEIGHT:
            self.vy = -self.vy
            self.y -= self.vy
        self.vy -= gravity
        self.x += self.vx
        self.y -= self.vy
        self.x += self.vx


class Bullet(Object):
    def __init__(self, screen: pygame.Surface, x, y, r, vx, vy):
        super().__init__(screen, x, y, vx, vy)
        self.r = r
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move_bullet(self):
        super().move(GRAVITY_TENSION)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            obj.hit()

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class Target(Object):
    def __init__(self, screen, x, y, vx, vy, live):
        """ Инициализация новой цели. """
        super().__init__(screen, x, y, vx, vy)
        self.live = live
        self.targettype = 'None'

    def hit(self):
        """Попадание шарика в цель."""
        global points
        global prev_points
        prev_points = points
        points += 1
        self.live -= 1
        if self.live == 0:
            self.new_target()

    def new_target(self):
        if self.targettype == 'Ball':
            new_target = Ball(screen,
                              randint(600, SCREEN_WIDTH - 100),
                              randint(300, SCREEN_HEIGHT - 100),
                              randint(20, 60),
                              randint(-1, 1),
                              randint(-1, 1),
                              1)
            self.erase()
            targets.remove(self)
            targets.append(new_target)



class Ball(Target):
    def __init__(self, screen: pygame.Surface, x, y, r, vx, vy, live):
        """ Инициализация новой цели. """
        super().__init__(screen, x, y, vx, vy, live)
        self.r = r
        self.color = RED
        self.screen = screen
        self.targettype = 'Ball'

    def move_ball(self):
        if self.live:
            super().move()
        else:
            pass

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def erase(self):
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r
        )


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.length = 20
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global bullets, bullet
        bullet += 1
        new_bullet = Bullet(self.screen,
                          40 * math.cos(self.an),
                          450 + 40 * math.sin(self.an),
                          10,
                          self.f2_power * math.cos(self.an) // 3,
                          - self.f2_power * math.sin(self.an) // 3)
        if event.pos[0]-new_bullet.x == 0:
            self.an = math.pi/2
        else:
            self.an = math.atan2((event.pos[1]-new_bullet.y), (event.pos[0]-new_bullet.x))
        bullets.append(new_bullet)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0]-20 == 0:
                self.an = math.pi/2
            else:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.polygon(
            self.screen,
            self.color,
            ((0, 440),
             (0, 460),
             (self.length * math.cos(self.an), 450 + self.length * math.sin(self.an) + 5),
             (self.length * math.cos(self.an), 450 + self.length * math.sin(self.an) - 5))
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.length += 1
            self.color = RED
        else:
            self.color = GREY
            self.length = 20

def score_points(points: int, prev_points: int):
    """
    Выводит на экран количество набранных очков
    :param score:
    """
    f = pygame.font.Font(None, 36)
    text = f.render('Score: ' + str(prev_points), 1, WHITE)
    screen.blit(text, (24, 18))
    text = f.render('Score: ' + str(points), 1, (180, 0, 0))
    screen.blit(text, (24, 18))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bullet = 0
prev_points = 0
points = 0
bullets = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
targets.append(Ball(screen,
                              randint(600, SCREEN_WIDTH - 100),
                              randint(300, SCREEN_HEIGHT - 100),
                              randint(20, 60),
                              randint(-1, 1),
                              randint(-1, 1),
                    1))

targets.append(Ball(screen,
                              randint(600, SCREEN_WIDTH - 100),
                              randint(300, SCREEN_HEIGHT - 100),
                              randint(20, 60),
                              randint(-1, 1),
                              randint(-1, 1),
                    1))

finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for t in targets:
        t.draw()
    for b in bullets:
        b.draw()

    score_points(points, prev_points)
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in bullets:
        b.move_bullet()
        for t in targets:
            t.move_ball()
            b.hittest(t)
    gun.power_up()

pygame.quit()
