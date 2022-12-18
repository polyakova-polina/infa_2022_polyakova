import pygame as pg
from solar_objects import Body

def draw_objects(screen, list_of_obj):
    """
    функция отрисовки объектов из list_of_obj на screen
    """
    for obj in list_of_obj:
        pg.draw.circle(screen, obj.colour, list(map(int, obj.q)), obj.r)


def draw_gui(screen, list_of_buttons):
    """
    функция отрисовки кнопок из list_of_buttons на screen
    """
    pass
