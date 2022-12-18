# coding: utf-8
# license: GPLv3

import pygame

class Button():
    """
    класс кнопки
    параметры: координаты на экране, прямоугольник формы, подпись, цвет
    """
    def __init__(self, role, rectangle, caption, colour):
        self.rect = rectangle
        self.caption = caption
        self.colour = colour
        self.role = role #1 - stop time, 2 - write down current data

    def click(self, x, y):
        """
        проверяет, находится ли event внутри прямоугольника кнопки
        """
        flag = False
        if self.rect[0] < x:
            if self.rect[0] + self.rect[2] > x:
                if self.rect[1] < y:
                    if self.rect[1] + self.rect[3] > y:
                        flag = True
        return flag

    def handle_events(self, event):
        """
        обработчик событий с кнопкой
        """
        func = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.click(event.pos[0], event.pos[1]) == True:
                func = self.role
        return func

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect, 0)
        font = pygame.font.Font(None, 30)
        text = font.render(self.caption, 1, (0, 0, 0))
        screen.blit(text, (self.rect[0] + 3, self.rect[1] + 3))
