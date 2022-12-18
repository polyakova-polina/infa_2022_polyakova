# coding: utf-8
# license: GPLv3

from solar_objects import Body
from solar_draw import draw_objects
from solar_input import get_data
from solar_input import write_down_data

from solar_vis import Button
import numpy as np
import pygame


FILE = 'sol_sist_data.txt'
FILE_WHERE = 'sol_sist_saved_data.txt'


class Manager():
    """
    класс менеджера приложения
    """
    def __init__(self, dt):
        """
        запускается менеджер и интерфейс
        """
        self.list_of_obj = []
        self.stop_b = Button(1, (0, 0, 120, 30), 'Pause/Play', (255, 0, 0))
        self.save_d_b = Button(2, (680, 0, 120, 30), 'Save data', (0, 255, 0))
        self.dt = dt
        self.pause = 0

    def set_file_from(self, file_from):
        """
        функция, устанавливающая файл, откуда будут считываться данные для тел
        обязательна к выполнению в начале работы приложения
        """
        data = get_data(file_from)
        for i in range(len(data)):
            m = data[i][0]
            r = data[i][1]
            colour = data[i][2]
            q = data[i][3]
            v = data[i][4]
            obj = Body(m, r, colour, q, v)
            self.list_of_obj.append(obj)
        

    def process(self, events, screen):
        """
        итерируемый через каждые dt времени код: перемещение планет, обновление
        их параметров, отрисовка, обработка событий на кнопках
        """
        done = self.react_events(events)
        if self.pause == 0:
            self.move_obj()
        self.draw(screen)
        return done

    def move_obj(self):
        """
        метод перемещения всех планет и обновления их параметров
        """
        for obj in self.list_of_obj:
            obj.move(self.list_of_obj, self.dt)
    
    def react_events(self, events):
        """
        метод обработки событий по всем кнопкам
        """
        done = False
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            if self.stop_b.handle_events(event) == 1:
                self.pause = (self.pause - 1) * (-1)
            if self.save_d_b.handle_events(event) == 2:
                write_down_data(FILE_WHERE, self.list_of_obj)
        return done

    def draw(self, screen):
        """
        отрисовка всех объектов на screen
        """
        for obj in self.list_of_obj:
            draw_objects(screen, self.list_of_obj)
        self.stop_b.draw(screen)
        self.save_d_b.draw(screen)

    def start(self):
        """
        запуск новых тел при изменении поля менеджера file_from
        """

pygame.init()
screen = pygame.display.set_mode([800, 600])
done = False
clock = pygame.time.Clock()

manager = Manager(dt=0.02)


"""
body1 = Body(5*10**13, 10, (0, 0, 0), [300, 300], [0, 3])
body2 = Body(5*10**13, 10, (0, 0, 0), [100, 300], [0, -3])
manager.list_of_obj.append(body1)
manager.list_of_obj.append(body2)
"""
manager.set_file_from(FILE)


while not done:
    clock.tick(1000)
    screen.fill([255, 255, 255])
    done = manager.process(pygame.event.get(), screen)
    pygame.display.flip()


pygame.quit()
