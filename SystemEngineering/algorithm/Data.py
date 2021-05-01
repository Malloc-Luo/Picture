# -*- coding: utf-8 -*-
from tools.vrp2json import vrp2json, load_json
import numpy as np
import matplotlib.pyplot as plt


class Data(object):
    VRP = "VRP"
    JSON = "JSON"

    def __init__(self, fname: str, ftype="VRP"):
        self.vrpf = fname
        self.tag = fname.split('.')[0]
        if ftype.lower() == Data.VRP.lower():
            self._json = vrp2json(fname)
        else:
            self._json = load_json(fname)
        self.extend()

    def extend(self):
        self._num = self._json['dimension']
        self._truck = self._json['trucks']
        self._capacity = self._json['capacity']
        self._value = self._json['Optimal value']
        self._point = self._json['points']
        self._x, self._y, self._r = [], [], []
        self._pair, self._demand = [], []
        for key, val in self._point.items():
            self._x.append(val[0])
            self._y.append(val[1])
            self._r.append(val[2])
            self._pair.append((val[0], val[1]))
            self._demand.append(val[2])

    def to_plot(self):
        plt.figure(0)
        # plt.grid()
        plt.axis('equal')
        plt.scatter(self._x, self._y, s=self._r)
        plt.scatter(self._x[0], self._y[0], s=120, c='r', marker='*')
        # plt.show()

    def plot_path(self, path):
        """ 绘制路线图，path为染色体
        [0, 1, 2, 3, 4, 0, 5, 6, 0, 7, 8, 0]
        """
        _path = np.array(path, dtype=np.int32)
        depot = [val[0] for val in np.argwhere(_path == 0)]
        subpath = [path[depot[i]: depot[i + 1] + 1] for i in range(len(depot) - 1)]
        plt.figure(0)
        plt.axis('equal')
        for _subpath in subpath:
            _x, _y = [self._x[pos] for pos in _subpath], [self._y[pos] for pos in _subpath]
            plt.plot(_x, _y)
        self.to_plot()
        plt.show()
        plt.savefig(self.tag + '.jpg')

    def generate_distance_matrix(self):
        """ 生成距离矩阵，各点之间的距离
        """
        self.matrix = np.zeros((self._num, self._num), dtype=np.float)
        for _x1 in range(self._num):
            for _x2 in range(self._num):
                self.matrix[_x1][_x2] = ((self._x[_x1] - self._x[_x2])**2 + (self._y[_x1] - self._y[_x2])**2)**(1 / 2)
        return self.matrix

    def get_dimension(self) -> list:
        return self._num

    def get_trucks(self) -> int:
        return self._truck

    def get_capacity(self) -> float:
        return self._capacity

    def get_optimize_value(self) -> float:
        return self._value

    def get_points(self) -> list:
        return self._point

    def get_pair_points(self) -> list:
        return self._pair

    def get_demands(self) -> list:
        return self._demand


if __name__ == '__main__':
    data = Data('A-n32-k5.vrp')
    print(data.generate_distance_matrix())
