# -*- coding: utf-8 -*-
import numpy as np
import random
import math
import copy


class TSP(object):
    """ TSP问题求解，动态规划求解TSP问题\n
    参考资料：
    https://www.jianshu.com/p/3d59231d66c0
    https://www.cnblogs.com/youmuchen/p/6879579.html
    https://blog.csdn.net/h9f3d3/article/details/80807064
    """
    def __init__(self, pointd: dict, start_node=0):
        self.pointd = pointd
        self.index = list(self.pointd.keys())
        self.point = list(self.pointd.values())
        self.distanceMatrix = self._generate_distance_matrix(self.point)
        self.start_node = start_node

    def transfer(self, sets):
        return sum([2**(s - 1) for s in sets])

    def _generate_distance_matrix(self, points: list) -> np.array:
        length = len(points)
        return np.array([[math.sqrt((points[_x1][0] - points[_x2][0])**2 + (points[_x1][1] - points[_x2][1])**2)
                        for _x1 in range(length)] for _x2 in range(length)])

    def _point_distance(self, _p1: int, _p2: int) -> float:
        return self.distanceMatrix[_p1][_p2]

    def _path_distance(self, path: list) -> float:
        """ [0, 1, 2, 3, 4, 0] 类似的 """
        distance = 0
        for _i in range(len(path) - 1):
            distance += self._point_distance(path[_i], path[_i + 1])
        return distance

    def _2_opt(self, step=1) -> list:
        """ 2-opt算法得到一个较优值（未必是最优值，只是相对于最初的好一点儿）
        Args:   iters: 迭代次数
        """
        _path = list(range(len(self.point))) + [0]
        _optimizedPath = _path
        _distance = self._path_distance(_optimizedPath)
        for start in range(1, len(_path) - 2):
            for end in range(start + step, len(_path)):
                if end - start == 1:
                    continue
                newPath = _path[: start] + _path[start: end][:: -1] + _path[end:]
                newDistance = self._path_distance(newPath)
                if newDistance < _distance:
                    _optimizedPath = newPath
                    _distance = newDistance
        return [int(self.index[v]) for v in _optimizedPath]

    def _dynamic_programming(self) -> list:
        """ 动态规划法求解，优点是精度高，缺点是时间复杂度是指数级别的
        所以当点的数量在8个以下时使用动态规划法求解
        """
        self.array = [[0] * (2**(len(self.distanceMatrix) - 1)) for i in range(len(self.distanceMatrix))]
        num = len(self.distanceMatrix)
        cities = list(range(num))
        cities.pop(cities.index(self.start_node))
        self.solve(self.start_node, cities)
        return self._get_index()

    def _get_index(self):
        _indexOrder = []
        lists = list(range(len(self.distanceMatrix)))
        _start = self.start_node
        while len(lists) > 0:
            _indexOrder.append(int(self.index[_start]))
            lists.pop(lists.index(_start))
            _next = self.array[_start][self.transfer(lists)]
            _start = _next
        _indexOrder.append(0)
        return _indexOrder

    def solve(self, node, future_sets):
        # 迭代终止条件，表示没有了未遍历节点，直接连接当前节点和起点即可
        if len(future_sets) == 0:
            return self.distanceMatrix[node][self.start_node]
        _minDistance = np.inf
        # node如果经过future_sets中节点，最后回到原点的距离
        distance = []
        # 遍历未经历的节点
        for i in range(len(future_sets)):
            s_i = future_sets[i]
            copy = future_sets[:]
            copy.pop(i)
            distance.append(self.distanceMatrix[node][s_i] + self.solve(s_i, copy))
        # 动态规划递推方程，利用递归
        _minDistance = min(distance)
        next_one = future_sets[distance.index(_minDistance)]
        # 未遍历节点集合
        c = self.transfer(future_sets)
        self.array[node][c] = next_one
        return _minDistance

    @staticmethod
    def opt(pointd: dict, threshold=7) -> list:
        tsp = TSP(pointd)
        if len(pointd) <= threshold:
            return tsp._dynamic_programming()
        else:
            return tsp._2_opt()


if __name__ == '__main__':
    pointd = {'0': [82, 76], '13': [84, 25], '27': [57, 69], '16': [88, 51], '12': [98, 52], '25': [9, 97], '4': [
        13, 7], '31': [98, 5]}
    import time
    start = time.time()
    print(TSP.opt(pointd))
    print(time.time() - start)
