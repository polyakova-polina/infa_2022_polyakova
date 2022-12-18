# coding: utf-8
# license: GPLv3

from solar_objects import Body

def write_down_data(file_to, list_of_obj):
    """
    функция, записывающая данные по телам в файл
    значения всех полей у каждого объекта из list_of_obj записываются в file_to
    """
    with open(file_to, 'w') as file:
        for obj in list_of_obj:
            mass = 'mass: ' + str(obj.m) + ' '
            rad = 'radius: ' + str(obj.r) + ' '
            str_col = [str(obj.colour[0]), str(obj.colour[1]), str(obj.colour[2])]
            colour = 'colour: ' + ' '.join(str_col) + ' '
            str_coord = [str(obj.q[0]), str(obj.q[1])]
            coord = 'coord: ' + ' '.join(str_coord) + ' '
            str_vel = [str(obj.v[0]), str(obj.v[1])]
            vel = 'vel: ' + ' '.join(str_vel) + ' '
            data = mass + rad + colour + coord + vel
            print(data, file=file)

def get_data(file_from):
    """
    функция чтения данных для тел из файла
    поля объектов list_of_obj заполняются данными из файла file_from
    """
    data = []
    with open (file_from) as file:
        
        for line in file.readlines():
            t_data = []
            for word in line.split():
                t_data.append(word)
            num_data = []
            num_data.append(float(t_data[1]))
            """
            какой-то баг с index: пишет, что out of range, хотя массив длиной
            явно больше 1
            """
            num_data.append(int(t_data[3]))
            num_data.append((int(t_data[5]), int(t_data[6]),
                             int(t_data[7])))
            num_data.append([float(t_data[9]), float(t_data[10])])
            num_data.append([float(t_data[12]), float(t_data[13])])
            data.append(num_data)
    return data
