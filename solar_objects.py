import numpy as np

G = 6.67 * 10**(-11)

class Body():
    """
    класс физических тел в симуляции: планет и звёзд
    базовые параметры: масса, радиус, цвет, координаты (массив), скорость (массив)
    """
    def __init__(self, mass, radius, colour, coordinates, velocities):
        self.m = mass
        self.r = radius
        self.colour = colour
        self.q = coordinates
        self.v = velocities

    def move(self, list_of_obj, dt):
        """
        метод движения тела
        для координат выполняется = скорость * dt + ускорение * dt^2 / 2,
        ускорение считается по всем другим телам из list_of_obj с помощью calc_acc
        для скоростей выполняется = ускорение * dt
        """
        a = self.calc_acc(list_of_obj)
        self.q[0] = self.q[0] + self.v[0] * dt + a[0] * (dt ** 2) / 2
        self.q[1] = self.q[1] + self.v[1] * dt + a[1] * (dt ** 2) / 2
        self.v[0] = self.v[0] + a[0] * dt
        self.v[1] = self.v[1] + a[1] * dt
    
    def calc_acc(self, list_of_obj):
        """
        метод, рассчитывающий ускорение тела
        """
        tot_acc = np.array([0, 0])
        for obj in list_of_obj:
            if self.q[0] != obj.q[0] or self.q[1] != obj.q[1]:
                q_0 = np.array(self.q)
                q = np.array(obj.q)
                r_to = q - q_0
                acc = G * obj.m / (np.linalg.norm(r_to) ** 3) * r_to
                tot_acc = tot_acc + acc
        return tot_acc.tolist()
