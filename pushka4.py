import math
from random import choice, randint

from pygame.draw import line, circle

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    global balls

    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса Ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if (WIDTH - self.x) <= self.r:
            self.x = WIDTH - self.r
            self.vx = -self.vx / 2
        if (HEIGHT - self.y) <= self.r:
            self.y = HEIGHT - self.r
            self.vy = (-self.vy) / 1.6
            self.vx = self.vx / 2
        self.vy -= 1
        self.x += self.vx
        self.y -= self.vy
        if (-1 < self.vy < 1) and (-1 < self.vx < 1):
            self.live += 1
            if self.live > 30:
                self.live = 0
                balls.remove(self)

    def draw(self):
        """ Рисует шарик. """
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r+1)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x-obj.x)**2+(self.y-obj.y)**2 < (self.r+obj.r)**2:
            return True
        return False


class Gun:
    def __init__(self, screen):
        """ Конструктор класса Gun. """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.len = 20

    def fire2_start(self):
        """ Заряжает пушку при нажатии кнопки мыши. """
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        target.bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши. """
        if event:
            try:
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
            except ZeroDivisionError:
                self.an = math.atan((event.pos[1] - 450) / 0.0000000000000001)
        if self.f2_on:
            self.color = YELLOW
        else:
            self.color = GREY

    def draw(self, event):
        """ Рисует пушку. Зависит от положения мыши. """
        if event:
            try:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
            except ZeroDivisionError:
                self.an = math.atan((event.pos[1] - 450) / 0.0000000000000001)
            line(screen, self.color, (40, 450), (40+self.len*math.cos(self.an), 450+self.len*math.sin(self.an)), 7)

    def power_up(self):
        """ Пушка заряжается. """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.len += 0.5
            self.color = YELLOW
        else:
            self.color = GREY
            self.len = 20


class Target:
    points = 0

    def __init__(self):
        """ Конструктор класса Target. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(5, 50)
        self.color = RED
        self.live = 1
        self.bullet = 0
        self.time = 0
        self.vx = randint(-150, 100)/100
        self.vy = randint(-150, 100)/100

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(5, 50)
        self.color = RED
        self.live = 1
        self.bullet = 0
        self.time = 0
        self.vx = randint(-150, 100) / 50
        self.vy = randint(-150, 100) / 50

    def target_in_array(self, targets):
            if len(targets < 2):
                targets.append(Target.new_target(self))

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 500+self.r or WIDTH-self.r < self.x:
            self.vx *= -1
        if self.y < self.r or HEIGHT-self.r < self.y:
            self.vy *= -1

    def hit(self):
        """Попадание шарика в цель."""
        self.points += 1

    def draw(self):
        """ Рисует цель. """
        if render:
            circle(screen, (0, 0, 0), (self.x, self.y), self.r+1)
            circle(screen, self.color, (self.x, self.y), self.r)

    def points_update(self):
        """ Выводит колличество очков на экран. """
        font = pygame.font.Font('freesansbold.ttf', 32)
        points = str(self.points)
        text = font.render(points, True, BLACK)
        screen.blit(text, (30, 50))

    def text_update(self, bull):
        """ Выводит колличество выстрелов на экран. """
        global render
        if not render:
            font = pygame.font.Font('freesansbold.ttf', 22)
            bullets = 'Вы уничтожили цель за ' + str(bull) + ' выстрелов'
            text = font.render(bullets, True, BLACK)
            screen.blit(text, (200, 275))
            self.time += 1
            if self.time > 45:
                render = True
                self.time = 0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
flag = 0
bull = 0
render = True
balls = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    target.draw()
    target.points_update()
    target.text_update(bull)
    if flag == 1:
        gun.draw(event_motion)
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
            event_motion = event
            flag = 1
    target.move()
    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            render = False
            if target.bullet:
                bull = target.bullet
                target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
